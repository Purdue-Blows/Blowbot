from discord.ext import commands
from typing import Any, Optional, Dict
from models.queue import Queue
from models.users import User
from utils.constants import SERVERS, bot, con
from services import youtube, spotify
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
    ctx: commands.Context,
    url: str,
    name: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    release_date: Optional[str] = None,
) -> None:
    # validate that url is a youtube url
    if not youtube.validate_youtube_url(url):
        await ctx.respond(URL_ERROR_MESSAGE, ephemeral=True)
        return
    song: Song = Song(
        name=name, artist=artist, url=url, album=album, release_date=release_date
    )
    # if a parameter is None, attempt to search the spotify api for it
    if name is None or artist is None or album is None or release_date is None:
        # Get any data possible from youtube
        if name is None or artist is None:
            song = await youtube.get_song_metadata_from_youtube(song)
        song = await spotify.get_song_metadata_from_spotify(song)
    # if the data isn't acquired, throw an error accordingly
    try:
        await Song.add(song=song)
    except Exception as e:
        await ctx.respond(DATABASE_ERROR_MESSAGE, ephemeral=True)
        return
    try:
        # Using the id of the song, add it to the queue table
        user = await User.retrieve_one(name=ctx.author.name)
        if user is None:
            user = await User.add(
                User(
                    name=ctx.author.name,
                    jazzle_streak=0,
                    jazz_trivia_correct=0,
                    jazz_trivia_incorrect=0,
                    jazz_trivia_percentage=0,
                )
            )
            if user is None:
                await ctx.respond(USER_ERROR_MESSAGE, ephemeral=True)
                return
        await Queue.add(
            Queue(
                song=song,
                audio=await youtube.download_song_from_youtube(song.url),
                user=user,
            )
        )
        # return a success message as confirmation
        await ctx.respond(SUCCESS_MESSAGE.format(ctx.author.name, song.name))
    except Exception as e:
        await ctx.respond(GENERAL_ERROR_MESSAGE, ephemeral=True)
    return
