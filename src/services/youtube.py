# Attempts to retrieve a song from youtube
from models.playlist import Playlist
from models.songs import Song
from models.users import User
from utils.constants import ydl, con, PURDUE_BLOWS_PLAYLIST_URL
from discord.ext import commands


# Attempts to retrieve the song metadata from a youtube url
async def get_song_metadata_from_youtube(song: Song) -> Song:
    # Validate that the url of the song is a youtube url
    if not await validate_youtube_url(song.url):
        return song

    # Retrieve song data using the youtube api
    info_dict = ydl.extract_info(song.url, download=False)

    # Return a new song object with any None fields updated appropriately
    if song.name is None:
        song.name = info_dict.get("title")

    if song.artist is None:
        if info_dict.get("artist") != None:
            song.artist = info_dict.get("artist")

    return song


# Validates that a url is a youtube url
async def validate_youtube_url(url: str) -> bool:
    if "https://www.youtube.com" in url:
        return True
    return False


# Parses song information into a youtube search
# ideal for finding the correct song
# Not necessary if urls are required
# async def create_youtube_search(song):
#     pass


# Attempts to download the song at url from youtube
async def download_song_from_youtube(url: str) -> bytes:
    # Use the youtube-dl library to download the song
    return ydl.download(url)


# Check if song exists in the youtube playlist
# NOTE: does not add the song to the playlist
async def check_song_in_playlist(song: Song) -> bool:
    # Retrieve playlist data using the youtube api
    playlist_dict = ydl.extract_info(song.url, download=False)

    # Iterate over videos in playlist
    for video in playlist_dict["entries"]:
        if not video:
            continue
        # If the video's title matches the song's title, return True
        # In the case that spotify does update the song name, it will just contain the song title
        # So these will likely be the same, but some testing should be done
        if song.name in video["title"]:
            return True
    return False


# A general utility method to ensure that the YouTube playlist and db are synced
async def sync_playlist(ctx: commands.Context, song: Song) -> bool:
    # Retrieve playlist data using the youtube api
    playlist_dict = ydl.extract_info(song.url, download=False)

    # Iterate over videos in playlist
    for video in playlist_dict["entries"]:
        if not video:
            continue
        # If the url isn't in the playlist table in the database, add it
        try:
            result = await Playlist.retrieve_one(video["url"])
            if result is None:
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
                            "An error occurred trying to add the user to the database",
                            ephemeral=True,
                        )
                        return False
                result = await Playlist.add(
                    Playlist(
                        song=Song(
                            name=video["title"],
                            artist=video["uploader"],
                            url=video["url"],
                        ),
                        audio=await download_song_from_youtube(video["url"]),
                        played=False,
                        user=user,
                    )
                )
                if result is None:
                    return False
        except Exception as e:
            return False
    return True
