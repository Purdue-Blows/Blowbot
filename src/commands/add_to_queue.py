from discord.ext import commands
from typing import Any, Optional, Dict
from models.queue import Queue
from models.users import User
from utils.constants import SERVERS, bot, con
from models.songs import Song
from services import youtube, spotify


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
        await ctx.respond("Url must be a valid YouTube url", ephemeral=True)
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
        await ctx.respond(
            "Sorry, that song's already in the database",
            ephemeral=True,
        )
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
                await ctx.respond(
                    "An error occurred while adding the user to the database",
                    ephemeral=True,
                )
                return
        await Queue.add(
            Queue(
                song=song,
                audio=await youtube.download_song_from_youtube(song.url),
                user=user,
            )
        )
        # return a success message as confirmation
        await ctx.respond(f"{ctx.author.name} added {song.name} to the queue!")
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}", ephemeral=True)
    return
