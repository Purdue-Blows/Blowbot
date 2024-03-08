# Attempts to retrieve a song from youtube
import os

from redis import DataError
from models.playlist import Playlist
from models.songs import Song
from models.users import User
from services import spotify_service
from services import youtube_service
from utils.constants import MAX_PLAYLIST_LENGTH, ydl, PURDUE_BLOWS_PLAYLIST_URL
from utils.functions import escape_special_characters, to_mp3_file
from discord.ext import commands

USER_ADD_ERROR_MESSAGE = "An error occurred while adding the user to the database"
YOUTUBE_DOWNLOAD_ERROR = "Could not download the information from youtube"


# Attempts to retrieve the song metadata from a youtube url
async def get_song_metadata_from_youtube(song: Song) -> Song:
    # Validate that the url of the song is a youtube url
    if not await validate_youtube_url(song.url):
        return song

    # Retrieve song data using the youtube api
    info_dict = ydl.extract_info(song.url, download=False)
    if info_dict is None:
        raise DataError(YOUTUBE_DOWNLOAD_ERROR)

    # Return a new song object with any None fields updated appropriately
    if song.name is None:
        song.name = info_dict.get("title")

    if song.artist is None:
        if info_dict.get("artist") != None:
            song.artist = info_dict.get("artist")

    if song.album is None:
        if info_dict.get("album") != None:
            song.album = info_dict.get("album")

    if song.release_date is None:
        if info_dict.get("release_date") != None:
            song.release_date = info_dict.get("release_date")

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
    # Use the yt-dlp library to download the song
    info_dict = ydl.extract_info(url, download=True)
    if info_dict is None:
        raise DataError(YOUTUBE_DOWNLOAD_ERROR)
    filepath = "%(title)s.%(ext)s"
    title = info_dict.get("title")
    if title != None:
        title = escape_special_characters(title)
    ext = info_dict.get("ext")
    if ext != None:
        ext = to_mp3_file(ext)
    downloaded_file_path = filepath % {"title": title, "ext": ext}
    # Rename file
    os.rename(
        os.path.join(os.getcwd(), "temp.mp3"),
        os.path.join(os.getcwd(), downloaded_file_path),
    )
    # Open file
    with open(os.path.join(os.getcwd(), downloaded_file_path), "rb") as file:
        audio = file.read()
    # Remove file
    os.remove(os.path.join(os.getcwd(), downloaded_file_path))
    return audio


# Check if song exists in the youtube playlist
# NOTE: does not add the song to the playlist
async def check_song_in_playlist(song: Song) -> bool:
    # Retrieve playlist data using the youtube api
    playlist_dict = ydl.extract_info(song.url, download=False)

    # Iterate over videos in playlist
    if playlist_dict is None:
        raise DataError(YOUTUBE_DOWNLOAD_ERROR)
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
async def sync_playlist(db) -> bool:
    # Ensure that the entire playlist can be retrieved
    ydl.params["playlist_items"] = "1-" + str(
        MAX_PLAYLIST_LENGTH
    )  # Not fetching any more than 1000 songs
    # Retrieve playlist data using the youtube api
    playlist_dict = ydl.extract_info(PURDUE_BLOWS_PLAYLIST_URL, download=False)

    if playlist_dict is None:
        raise DataError(YOUTUBE_DOWNLOAD_ERROR)

    ydl.params["playlist_items"] = "1"  # Back to fetching one song

    # print(playlist_dict)
    # Iterate over videos in playlist
    for video in playlist_dict["entries"]:
        if not video:
            continue
        # If the url isn't in the playlist table in the database, add it
        try:
            print("Attempting to retrieve " + video["title"] + "from playlist")
            song = await Song.retrieve_one(url=video["webpage_url"])
            result = None
            if song:
                result = await Playlist.retrieve_one(db, song_id=song.id)
            if result is None:
                # Create a song for the url
                song = Song(
                    name=video["title"],
                    artist=video["uploader"],
                    url=video["webpage_url"],
                )
                # Ensure song data is correct
                if (
                    song.name is None
                    or song.artist is None
                    or song.album is None
                    or song.release_date is None
                ):
                    # Get any data possible from youtube
                    song = await youtube_service.get_song_metadata_from_youtube(song)
                    print(song.to_string())
                    # Get any data possible from spotify
                    if (
                        song.name is None
                        or song.artist is None
                        or song.album is None
                        or song.release_date is None
                    ):
                        song = await spotify_service.get_song_metadata_from_spotify(
                            song
                        )
                # Download the video associated with the url
                # Using the id of the song, add it to the queue table
                print("Attempting to add " + video["title"] + "from playlist")
                result = await Playlist.add(
                    db,
                    Playlist(
                        song=song,
                        # audio=await download_song_from_youtube(video["webpage_url"]),
                        # playlist_name="Purdue Blows",
                        # playlist_num=0,
                        played=False,
                        user=None,
                    ),
                )
                print(result)
                if result is None:
                    print("Could not add " + video["title"] + "to playlist")
                    return False
        except Exception as e:
            print("An error occurred while syncing the playlist: " + str(e))
            return False
    return True
