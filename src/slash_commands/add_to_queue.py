import traceback
from discord.ext import commands
from typing import Any, Optional, Dict
from models.queue import Queue
from models.users import User
from services import spotify_service
from utils.constants import SERVERS, Session, bot, ydl, spotify
from services import youtube_service
from utils.messages import NO_GUILD_ERROR
from models.songs import Song

# Define constant string literals
URL_ERROR_MESSAGE = "Url must be a valid YouTube url"
DATABASE_ERROR_MESSAGE = "Sorry, that song's already in the database"
USER_ERROR_MESSAGE = "An error occurred while adding the user to the database"
GENERAL_ERROR_MESSAGE = "Sorry, an error occurred while adding the song to the queue"
SUCCESS_MESSAGE = "{} added {} to the queue!"


# Adds a song to the queue
@bot.slash_command(
    name="add_to_queue", description="Add a song to Blowbot's queue", guild_ids=SERVERS
)
async def add_to_queue(
    ctx,
    url: str,
    name: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    release_date: Optional[str] = None,
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # validate that url is a youtube url
        if not youtube_service.validate_youtube_url(url):
            await ctx.respond(URL_ERROR_MESSAGE, ephemeral=True)
            return
        song: Song = Song(
            name=name, artist=artist, url=url, album=album, release_date=release_date
        )
        # if a parameter is None, attempt to search the spotify api for it
        if name is None or artist is None or album is None or release_date is None:
            # Get any data possible from youtube
            if name is None or artist is None:
                song = await youtube_service.get_song_metadata_from_youtube(ydl, song)
            song = await spotify_service.get_song_metadata_from_spotify(spotify, song)
        # if the data isn't acquired, throw an error accordingly
        try:
            await Song.add(session, song=song)
        except Exception as e:
            await ctx.respond(DATABASE_ERROR_MESSAGE, ephemeral=True)
            traceback.print_exc()
            return
        try:
            # Using the id of the song, add it to the queue table
            user = await User.retrieve_one(
                session, guild_id=ctx.guild.id, name=ctx.author.name
            )
            if user is None:
                user = await User.add(
                    session,
                    User(
                        name=ctx.author.name,
                        jazzle_streak=0,
                        jazz_trivia_correct=0,
                        jazz_trivia_incorrect=0,
                        jazz_trivia_percentage=0,
                    ),
                )
                if user is None:
                    await ctx.respond(USER_ERROR_MESSAGE, ephemeral=True)
                    return
            await Queue.add(
                session,
                Queue(
                    song=song,
                    user=user,
                ),
            )
            # return a success message as confirmation
            await ctx.send(SUCCESS_MESSAGE.format(ctx.author.name, song.name))
        except Exception as e:
            await ctx.respond(GENERAL_ERROR_MESSAGE, ephemeral=True)
            traceback.print_exc()
        return
