from models.playlist import Playlist
from models.songs import Song
from models.users import User
from services import spotify_service
from services import youtube_service
from utils.constants import DB_CLIENT, SERVERS, bot, ydl, spotify
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
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


# Add a song to the Purdue Blows playlist
@bot.command(
    name="add_to_playlist",
    description="Adds a link to the Purdue Blows playlist",
    guild_ids=SERVERS,
)
async def add_to_playlist(
    ctx: commands.Context,
    url: str,
    playlist_name: str,
    name: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    release_date: Optional[str] = None,
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # validate that url is a youtube url
    if not await youtube_service.validate_youtube_url(url):
        await ctx.send(URL_ERROR_MESSAGE, ephemeral=True)
        return
    song = Song(
        name=name, artist=artist, url=url, album=album, release_date=release_date
    )
    # if a parameter is None, attempt to search the spotify api for it
    if name is None or artist is None or album is None or release_date is None:
        # Get any data possible from youtube
        song = await youtube_service.get_song_metadata_from_youtube(ydl, song)
        print(song.to_string())
        # Get any data possible from spotify
        if name is None or artist is None or album is None or release_date is None:
            song = await spotify_service.get_song_metadata_from_spotify(spotify, song)
    print(song.to_string())
    # if the data isn't acquired, throw an error accordingly
    if song.name is None and song.artist is None:
        await ctx.send(
            NAME_AND_ARTIST_ERROR_MESSAGE,
            ephemeral=True,
        )
        return
    if song.name is None:
        await ctx.send(NAME_ERROR_MESSAGE, ephemeral=True)
        return
    if song.artist is None:
        await ctx.send(ARTIST_ERROR_MESSAGE, ephemeral=True)
        return
    try:
        print("Trying to add a song")
        await Song.add(song=song)
    except Exception as e:
        await ctx.send(SONG_EXISTS_ERROR_MESSAGE, ephemeral=True)
        return
    try:
        user = await User.retrieve_one(db, name=ctx.author.name)
    except Exception as e:
        await ctx.send(USER_RETRIEVAL_ERROR_MESSAGE, ephemeral=True)
        return
    try:
        if user is None:
            user = await User.add(
                db,
                User(
                    name=ctx.author.name,
                    jazzle_streak=0,
                    jazz_trivia_correct=0,
                    jazz_trivia_incorrect=0,
                    jazz_trivia_percentage=0,
                ),
            )
            if user is None:
                await ctx.send(USER_ADD_ERROR_MESSAGE, ephemeral=True)
                return
    except Exception as e:
        await ctx.send(USER_ADD_ERROR_MESSAGE, ephemeral=True)
        return
    try:
        await Playlist.add(
            db,
            Playlist(
                song=song,
                playlist_name=playlist_name,
                played=False,
                user=user,
            ),
        )
        # return a success message as confirmation
        await ctx.send(
            SUCCESS_MESSAGE.format(author_name=ctx.author.name, song_name=song.name)
        )
    except Exception as e:
        await ctx.send(SONG_ADD_ERROR_MESSAGE, ephemeral=True)
    return
