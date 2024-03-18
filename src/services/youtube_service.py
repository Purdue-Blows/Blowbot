from sqlalchemy.exc import IntegrityError

# Attempts to retrieve a song from youtube
import os
from yt_dlp import YoutubeDL
from services.download_song_from_youtube import download_song_from_youtube
from models.playlist import Playlist
from models.songs import Song
from services import spotify_service
from models.model_fields import SongFields
from utils.constants import (
    MAX_PLAYLIST_LENGTH,
    PURDUE_BLOWS_PLAYLISTS,
    PlaylistNames,
    spotify,
    gemini,
)
from utils.escape_special_characters import escape_special_characters
from utils.to_mp3_file import to_mp3_file
from discord.ext import commands

USER_ADD_ERROR_MESSAGE = "An error occurred while adding the user to the database"
YOUTUBE_DOWNLOAD_ERROR = "Could not download the information from youtube"


# Attempts to retrieve the song metadata from a youtube url
async def get_song_metadata_from_youtube(ydl: YoutubeDL, song: Song) -> Song:
    # Validate that the url of the song is a youtube url
    if not await validate_youtube_url(song.url):  # type: ignore
        return song

    # Retrieve song data using the youtube api
    info_dict = ydl.extract_info(song.url, download=False)
    if info_dict is None:
        raise ValueError(YOUTUBE_DOWNLOAD_ERROR)

    # print("YOUTUBE")
    # print(info_dict)

    # Return a new song object with any None fields updated appropriately
    if song.name is None:
        if info_dict.get(SongFields.NAME.name) != None:
            song.name = info_dict.get(SongFields.NAME.name)  # type: ignore

    # YT-ARTIST data isn't as consistent as spotify
    if song.artist is None:
        artist = await gemini.generate_content_async(
            f"""
        Here is the youtube video title and description of a song. I want you to extract 
        the artist from it and ONLY return the artist as an output.
        {info_dict.get("title")} {info_dict.get("description")}
        """
        )
        # if info_dict.get(SongFields.ARTIST.name) != None:
        song.artist = artist.text  # type: ignore

    if song.album is None:
        if info_dict.get(SongFields.ALBUM.name) != None:
            song.album = info_dict.get(SongFields.ALBUM.name)  # type: ignore

    if song.release_date is None:
        if info_dict.get(SongFields.RELEASE_DATE.name) != None:
            song.release_date = info_dict.get(SongFields.RELEASE_DATE.name)  # type: ignore

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


# Check if song exists in the youtube playlist
# NOTE: does not add the song to the playlist
async def check_song_in_playlist(ydl: YoutubeDL, song: Song) -> bool:
    # Retrieve playlist data using the youtube api
    playlist_dict = ydl.extract_info(song.url, download=False)

    # Iterate over videos in playlist
    if playlist_dict is None:
        raise ValueError(YOUTUBE_DOWNLOAD_ERROR)
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
# TODO: make this sync_database instead; this should sync ALL yt data with the database
async def sync_playlist(
    session, guild_id, ydl: YoutubeDL, playlist_name: PlaylistNames
) -> bool:
    # Ensure that the entire playlist can be retrieved
    ydl.params["playlist_items"] = "1-" + str(
        MAX_PLAYLIST_LENGTH
    )  # Not fetching any more than 1000 songs
    # Retrieve playlist data using the youtube api
    playlist_dict = ydl.extract_info(
        PURDUE_BLOWS_PLAYLISTS[playlist_name], download=False
    )

    if playlist_dict is None:
        raise ValueError(YOUTUBE_DOWNLOAD_ERROR)

    ydl.params["playlist_items"] = "1"  # Back to fetching one song

    # print(playlist_dict)
    # Iterate over videos in playlist
    for video in playlist_dict["entries"]:
        if not video:
            continue
        # If the url isn't in the playlist table in the database, add it
        try:
            print("Attempting to retrieve " + video["title"] + "from playlist")
            song = await Song.retrieve_one(session, url=video["webpage_url"])
            result = None
            if song:
                result = await Playlist.retrieve_one(session, guild_id=guild_id, song_id=song.id)  # type: ignore
            if result is None:
                # Create a song for the url
                song = Song(
                    name=video["title"],
                    # artist=video["uploader"],
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
                    song = await get_song_metadata_from_youtube(ydl, song)
                    # Get any data possible from spotify
                    if (
                        song.name is None
                        or song.artist is None
                        or song.album is None
                        or song.release_date is None
                    ):
                        song = await spotify_service.get_song_metadata_from_spotify(
                            spotify, song
                        )
            if song.audio is None:
                song.audio = await download_song_from_youtube(ydl, video["webpage_url"])  # type: ignore
            # Download the video associated with the url
            # Using the id of the song, add it to the queue table
            print("Attempting to add " + video["title"] + "from playlist")
            result = await Playlist.add(
                session,
                Playlist(
                    song=song,
                    playlist_name=playlist_name,
                    playlist_num=video["playlist_index"],
                    played=False,
                    user=None,
                    guild_id=guild_id,
                ),
            )
            print(result)
            if result is None:
                print("Could not add " + video["title"] + "to playlist")
                return False
        except IntegrityError as e:
            continue
        except Exception as e:
            print(type(e))
            print("An error occurred while syncing the playlist: " + str(e))
            return False
    return True
