from enum import Enum
import os
from pickle import NONE
import subprocess
import discord
import sqlite3
from multiprocessing import Process
import multiprocessing
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from models.model_fields import (
    PlaybackFields,
    PlaylistFields,
    QueueFields,
    SongFields,
    UserFields,
)

from utils.escape_special_characters import escape_special_characters
from utils.to_mp3_file import to_mp3_file

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if not load_dotenv(os.path.join(BASE_DIR, ".env")):
    raise Exception("Could not parse the .env file")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
assert DISCORD_TOKEN != None
CLIENT_ID: int = int(os.getenv("CLIENT_ID"))  # type: ignore
assert CLIENT_ID != None
PURDUE_BLOWS_SERVER_ID: int = int(os.getenv("PURDUE_BLOWS_SERVER_ID"))  # type: ignore
assert PURDUE_BLOWS_SERVER_ID != None
BOT_DEBUGGING_SERVER_ID: int = int(os.getenv("BOT_DEBUGGING_SERVER_ID"))  # type: ignore
assert BOT_DEBUGGING_SERVER_ID != None
SERVERS = [PURDUE_BLOWS_SERVER_ID, BOT_DEBUGGING_SERVER_ID]
# MONGO_URI = os.getenv("MONGO_URI")
# assert MONGO_URI
# MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT"))  # type: ignore
SPOTIFY_ID = os.getenv("SPOTIFY_ID")
assert SPOTIFY_ID != None
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
assert SPOTIFY_SECRET != None
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
assert SPOTIFY_REDIRECT_URI != None
MAX_MESSAGE_LENGTH = 2000

PURDUE_BLOWS_CHANNEL_IDS = {
    "general": 1148646209586745391,
    "commands": 1210003092356210779,
    "vibe": 1212457675087024148,
}

BOT_DEBUGGING_SERVER_CHANNEL_IDS = {
    "general": 909075276774907947,
    "general_voice": 909075276774907948,
    "general_voice_2": 1214048071034474547,
}

# PURDUE_BLOWS_PLAYLIST_URL = "https://open.spotify.com/playlist/6MPc4BFOUT9mUIz0G6ME4B?si=z4XGO1ELRLqfS3TyrmbiHA&pt_success=1&nd=1&dlsi=11e24dc164584f44"
# PURDUE_BLOWS_PLAYLIST_URI = "spotify:playlist:6MPc4BFOUT9mUIz0G6ME4B"
COMMUNITY_PLAYLIST_URL = (
    "https://www.youtube.com/playlist?list=PLDLRACxotfNFS5nL608HiV84mN0RkUpUY"
)

FAKE_BOOK_PLAYLIST_URL = (
    "https://www.youtube.com/playlist?list=PLDLRACxotfNFps5vTE_qExW077RCmo1vX"
)


class PlaylistNames(Enum):
    COMMUNITY = "community"
    FAKE_BOOK = "fake_book"

    @classmethod
    def from_string(cls, value: str | None) -> "PlaylistNames":
        for playlist in cls:
            if playlist.value == value:
                return playlist
        raise ValueError(f"No playlist with value '{value}' exists.")

    def __str__(self) -> str:
        return self.value


class CurrentlyPlaying(Enum):
    PLAYLIST = "playlist"
    QUEUE = "queue"
    NONE = "none"

    @classmethod
    def from_string(cls, value: str | None) -> "CurrentlyPlaying":
        for playing in cls:
            if playing.value == value:
                return playing
        raise ValueError(f"No currently playing with value '{value}' exists.")

    def __str__(self) -> str:
        return self.value


PURDUE_BLOWS_PLAYLISTS = {
    # Playlist name: vc id associated with playlist
    PlaylistNames.COMMUNITY: COMMUNITY_PLAYLIST_URL,
    PlaylistNames.FAKE_BOOK: FAKE_BOOK_PLAYLIST_URL,
}

MAX_PLAYLIST_LENGTH = 1000

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Initialize bot
bot = commands.Bot(command_prefix="/", intents=intents)
assert bot != None
# Remove default help command
bot.remove_command("help")

# Initialize spotify
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRET
    )
)
assert spotify != None


# Start the mongod client
def start_mongod_client():
    return subprocess.call(["mongod"], shell=False)


mongod = Process(target=start_mongod_client)
mongod.start()

# Host database
DB_CLIENT = AsyncIOMotorClient(MONGO_HOST, MONGO_PORT)
assert DB_CLIENT != None
# I want a different database based on the server id
# That way each server has their own database
# db = client.blowbot
# assert db != None


async def initialize_collections(db):
    # Initialize the songs db (globally accessible for each server)
    # Note that the songs db has a songs collection
    if not await DB_CLIENT.songs.songs.index_information():
        await DB_CLIENT.songs.songs.create_index(SongFields.NAME.name)
        await DB_CLIENT.songs.songs.create_index(SongFields.ARTIST.name)
        await DB_CLIENT.songs.songs.create_index(SongFields.URL.name, unique=True)
        await DB_CLIENT.songs.songs.create_index(SongFields.ALBUM.name)
        await DB_CLIENT.songs.songs.create_index(SongFields.RELEASE_DATE.name)
        await DB_CLIENT.songs.songs.create_index(SongFields.AUDIO.name)

    if not await db.users.index_information():
        await db.users.create_index(UserFields.NAME.name, unique=True)
        await db.users.create_index(UserFields.JAZZLE_STREAK.name)
        await db.users.create_index(UserFields.JAZZ_TRIVIA_CORRECT.name)
        await db.users.create_index(UserFields.JAZZ_TRIVIA_INCORRECT.name)
        await db.users.create_index(UserFields.JAZZ_TRIVIA_PERCENTAGE.name)

    if not await db.playlist.index_information():
        await db.playlist.create_index(PlaylistFields.SONG_ID.name)
        await db.playlist.create_index(PlaylistFields.USER_ID.name)
        await db.playlist.create_index(PlaylistFields.PLAYED.name)
        await db.playlist.create_index(PlaylistFields.PLAYLIST_NUM.name)
        await db.playlist.create_index(
            PlaylistFields.PLAYLIST_NAME.name
        )  # For keeping track of the order that songs were played in.
        # All playlist_nums are cleared once a playlist has been cycled through
        # The default for playlist_num is the position of the video in the yt playlist

    if not await db.queue.index_information():
        await db.queue.create_index(QueueFields.SONG_ID.name)
        await db.queue.create_index(QueueFields.USER_ID.name)
        await db.queue.create_index(
            QueueFields.QUEUE_NUM.name
        )  # Order and retrieve documents by their queue_num
        # To avoid a global var, retrieval is handled by getting the least number in the queue that hasn't been played
        await db.queue.create_index(
            QueueFields.PLAYED.name
        )  # NOTE: the queue never has more than 50 songs in it; if it does, on adding to it the one
        # with the smallest queue_num that has been played is deleted

    if not await db.playback.index_information():
        await db.playback.create_index(PlaybackFields.CURRENT_PLAYLIST.name)
        await db.playback.create_index(PlaybackFields.CURRENT_PLAYLIST_INDEX.name)
        await db.playback.create_index(PlaybackFields.CURRENTLY_PLAYING.name)

    # Set validation rules for collections
    # Ensure that the song_id and user_id fields always map to valid instances in the song and user collections
    # await db.playlist.create_index(
    #     [(PlaylistFields.USER_ID.name, 1)],
    #     unique=True,
    #     partialFilterExpression={PlaylistFields.USER_ID.name: {"$exists": True}},
    # )
    # await db.queue.create_index(
    #     [(QueueFields.USER_ID.name, 1)],
    #     unique=True,
    #     partialFilterExpression={QueueFields.USER_ID.name: {"$exists": True}},
    # )
    # await db.playlist.create_index(
    #     [(PlaylistFields.SONG_ID.name, 1)],
    #     unique=True,
    #     partialFilterExpression={PlaylistFields.SONG_ID.name: {"$exists": True}},
    # )
    # await db.queue.create_index(
    #     [(QueueFields.SONG_ID.name, 1)],
    #     unique=True,
    #     partialFilterExpression={QueueFields.SONG_ID.name: {"$exists": True}},
    # )


# if not os.path.exists(os.path.join(BASE_DIR, DB)):
#     con = sqlite3.connect(DB)
#     cur = con.cursor()
#     cur.execute(
#         """
#         CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, jazzle_streak INTEGER,
#         jazz_trivia_correct INTEGER, jazz_trivia_incorrect INTEGER,
#         jazz_trivia_percentage REAL)
#         """
#     )
#     cur.execute(
#         """
#         CREATE TABLE songs(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, artist TEXT, url TEXT UNIQUE, album TEXT NULL,
#         release_date TEXT NULL)
#         """
#     )
#     cur.execute(
#         """
#         CREATE TABLE playlist(id INTEGER PRIMARY KEY AUTOINCREMENT, song_id INTEGER, song BLOB, played BOOLEAN, user_id INTEGER NULL,
#         FOREIGN KEY(song_id) REFERENCES songs(id))
#         """
#     )
#     cur.execute(
#         """
#         CREATE TABLE queue(id INTEGER PRIMARY KEY AUTOINCREMENT, song_id INTEGER, song BLOB, user_id INTEGER,
#         FOREIGN KEY(song_id) REFERENCES songs(id))
#         """
#     )
#     cur.execute("PRAGMA foreign_keys = ON")
# else:
#     con = sqlite3.connect(DB)
# assert con != None

# Initialize yt-dlp
yt_opts = {
    "best-audio": True,
    "extract_audio": True,
    "noplaylist": True,
    "audio-format": "mp3",
    "audio-quality": 0,
    "outtmpl": "temp.%(ext)s",  # Temporary video title wo/ invalid characters; gets renamed appropriately
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        },
    ],
    "restrict_filenames": True,
    "playlist_items": "1",
}
ydl = yt_dlp.YoutubeDL(yt_opts)
assert ydl != None
