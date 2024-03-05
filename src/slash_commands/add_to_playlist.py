from models.playlist import Playlist
from models.songs import Song
from models.users import User
from utils.constants import SERVERS, bot
from services import youtube, spotify
from discord.ext import commands
from typing import Optional

# Define constant string literals
URL_ERROR_MESSAGE = "Url must be a valid YouTube url"
NAME_AND_ARTIST_ERROR_MESSAGE = "Sorry, the name and artist of the song couldn't be determined; if you want to add the song, please provide the name and artist"
NAME_ERROR_MESSAGE = "Sorry, the name of the song couldn't be determined; if you want to add the song, please provide the name"
ARTIST_ERROR_MESSAGE = "Sorry, the name of the artist couldn't be determined; if you want to add the song, please provide the name"
SONG_EXISTS_ERROR_MESSAGE = "Sorry, that song's already in the database"
USER_RETRIEVAL_ERROR_MESSAGE = "Failed to retrieve the user"
USER_ADD_ERROR_MESSAGE = "An error occurred while adding the user to the database"
SONG_ADD_ERROR_MESSAGE = (
    "Sorry, an error occurred while adding the song to the playlist"
)
SUCCESS_MESSAGE = "{author_name} added {song_name} to the Purdue Blows playlist"


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
        await ctx.respond(URL_ERROR_MESSAGE, ephemeral=True)
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
    if song.name is None and song.artist is None:
        await ctx.respond(
            NAME_AND_ARTIST_ERROR_MESSAGE,
            ephemeral=True,
        )
        return
    if song.name is None:
        await ctx.respond(NAME_ERROR_MESSAGE, ephemeral=True)
        return
    if song.artist is None:
        await ctx.respond(ARTIST_ERROR_MESSAGE, ephemeral=True)
        return
    try:
        print("Trying to add a song")
        await Song.add(song=song)
    except Exception as e:
        await ctx.respond(SONG_EXISTS_ERROR_MESSAGE, ephemeral=True)
        return
    try:
        user = await User.retrieve_one(name=ctx.author.name)
    except Exception as e:
        await ctx.respond(USER_RETRIEVAL_ERROR_MESSAGE, ephemeral=True)
        return
    try:
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
                await ctx.respond(USER_ADD_ERROR_MESSAGE, ephemeral=True)
                return
    except Exception as e:
        await ctx.respond(USER_ADD_ERROR_MESSAGE, ephemeral=True)
        return
    try:
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
            SUCCESS_MESSAGE.format(author_name=ctx.author.name, song_name=song.name)
        )
    except Exception as e:
        await ctx.respond(SONG_ADD_ERROR_MESSAGE, ephemeral=True)
    return
