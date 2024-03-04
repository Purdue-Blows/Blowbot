from tkinter import NO
from models.playlist import Playlist
from models.songs import Song
from models.users import User
from utils.constants import SERVERS, bot
from services import youtube, spotify
from discord.ext import commands
from typing import Optional


# Add a song to the Purdue Blows playlist
@bot.slash_command(
    name="add_to_playlist",
    description="Adds a link to the Purdue Blows playlist",
    guild_ids=SERVERS,
)
async def add_to_playlist(
    ctx: commands.Context,
    url: str,
    name: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    release_date: Optional[str] = None,
) -> None:
    # validate that url is a youtube url
    if not await youtube.validate_youtube_url(url):
        await ctx.respond("Url must be a valid YouTube url", ephemeral=True)
        return
    song = Song(
        name=name, artist=artist, url=url, album=album, release_date=release_date
    )
    # if a parameter is None, attempt to search the spotify api for it
    if name is None or artist is None or album is None or release_date is None:
        # Get any data possible from youtube
        if name is None or artist is None:
            song = await youtube.get_song_metadata_from_youtube(song)
            print(song.to_string())
        song = await spotify.get_song_metadata_from_spotify(song)
    print(song.to_string())
    # if the data isn't acquired, throw an error accordingly
    if song.name is None:
        await ctx.respond(
            "Sorry, the name of the song couldn't be determined; if you want to add the song, please provide the name",
            ephemeral=True,
        )
        return
    if song.artist is None:
        await ctx.respond(
            "Sorry, the name of the artist couldn't be determined; if you want to add the song, please provide the name",
            ephemeral=True,
        )
        return
    try:
        print("Trying to add a song")
        await Song.add(song=song)
    except Exception as e:
        await ctx.respond(
            "Sorry, that song's already in the database",
            ephemeral=True,
        )
        return
    try:
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
        await Playlist.add(
            Playlist(
                song=song,
                audio=await youtube.download_song_from_youtube(song.url),
                played=False,
                user=user,
            )
        )
        # return a success message as confirmation
        await ctx.respond(
            f"{ctx.author.name} added {song.name} to the Purdue Blows playlist"
        )
    except Exception as e:
        await ctx.respond(
            "Sorry, an error occurred while adding the song to the playlist",
            ephemeral=True,
        )
