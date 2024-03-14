from enum import Enum
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import google.generativeai as genai


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
from sqlalchemy import (
    BLOB,
    Boolean,
    Column,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    LargeBinary,
    String,
    Table,
    create_engine,
    inspect,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
import subprocess
import platform

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
# MONGO_HOST = os.getenv("MONGO_HOST")
# MONGO_PORT = int(os.getenv("MONGO_PORT"))  # type: ignore
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
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
            if str(playlist.value) == str(value):
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
            if str(playing.value) == str(value):
                return playing
        raise ValueError(f"No currently playing with value '{value}' exists.")

    def __str__(self) -> str:
        return self.value


PURDUE_BLOWS_PLAYLISTS = {
    # Playlist name: vc id associated with playlist
    PlaylistNames.COMMUNITY: COMMUNITY_PLAYLIST_URL,
    PlaylistNames.FAKE_BOOK: FAKE_BOOK_PLAYLIST_URL,
}

# SPOTIFY_USERNAME = os.getenv("SPOTIFY_USERNAME")

MAX_PLAYLIST_LENGTH = 1000

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Connect to the Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
gemini = genai.GenerativeModel("gemini-pro")
assert gemini != None

# Initialize bot
bot = commands.Bot(command_prefix="/", intents=intents)
assert bot != None
# Remove default help command
# bot.remove_command("help")

# Initialize spotify
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRET
    )
)
assert spotify != None


# Start the database client
# Create engine
engine = create_engine(
    f"postgresql+psycopg://{DB_USERNAME}:{DB_PASSWORD}@localhost:{DB_PORT}/{DB_NAME}"
)
assert engine != None

# Create session
Session = sessionmaker(bind=engine)
assert Session != None
Base = declarative_base()
assert Base != None
# session = Session()

# Initialize database client
# DB_CLIENT = session
# assert DB_CLIENT != None
# I want a different database based on the server id
# That way each server has their own database
# db = client.blowbot
# assert db != None


# def start_db():
#     system = platform.system()
#     if system == "Windows":
#         subprocess.run(["psq;", "start", "-D", "C:/Program Files/PostgreSQL/13/data"])
#     elif system == "Linux":
#         subprocess.run(["psql", "start", "-D", "/usr/local/var/postgres"])
#     elif system == "Darwin":
#         subprocess.run(["psql", "start", "-D", "/usr/local/var/postgres"])
#     else:
#         raise Exception(f"{system} is not supported.")


# start_db()


# def stop_db():
#     system = platform.system()
#     if system == "Windows":
#         subprocess.run(["psql", "stop", "-D", "C:/Program Files/PostgreSQL/13/data"])
#     elif system in ["Linux", "Darwin"]:
#         subprocess.run(["psql", "stop", "-D", "/usr/local/var/postgres"])
#     else:
#         raise Exception(f"{system} is not supported.")


async def initialize_collections(engine):
    # Initialize the songs db (globally accessible for each server)
    # Note that the songs db has a songs table
    # metadata = MetaData()

    # if not inspect(engine).has_table("songs"):
    #     songs_table = Table(
    #         "songs",
    #         metadata,
    #         Column("id", Integer, primary_key=True),
    #         Column("name", String),
    #         Column("artist", String),
    #         Column("url", String, unique=True),
    #         Column("album", String),
    #         Column("release_date", String),
    #         Column("audio", LargeBinary),
    #     )
    #     metadata.create_all(engine)

    # if not inspect(engine).has_table("users"):
    #     users_table = Table(
    #         "users",
    #         metadata,
    #         Column("id", Integer, primary_key=True),
    #         Column("name", String, unique=True),
    #         Column("jazzle_streak", Integer),
    #         Column("jazz_trivia_correct", Integer),
    #         Column("jazz_trivia_incorrect", Integer),
    #         Column("jazz_trivia_percentage", Float),
    #         Column("guild_id", Integer, unique=True),
    #     )
    #     metadata.create_all(engine)

    # if not inspect(engine).has_table("playlist"):
    #     playlist_table = Table(
    #         "playlist",
    #         metadata,
    #         Column("id", Integer, primary_key=True),
    #         Column("song_id", Integer, ForeignKey("songs.id", ondelete="CASCADE")),
    #         Column("played", Boolean),
    #         Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    #         Column("guild_id", Integer),
    #     )
    #     metadata.create_all(engine)

    # if not inspect(engine).has_table("queue"):
    #     queue_table = Table(
    #         "queue",
    #         metadata,
    #         Column("id", Integer, primary_key=True),
    #         Column("song_id", Integer, ForeignKey("songs.id", ondelete="CASCADE")),
    #         Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    #         Column("guild_id", Integer),
    #     )
    #     metadata.create_all(engine)

    # if not inspect(engine).has_table("playback"):
    #     playback_table = Table(
    #         "playback",
    #         metadata,
    #         Column("id", Integer, primary_key=True),
    #         Column("current_playlist", String),
    #         Column("current_playlist_index", Integer),
    #         Column("currently_playing", String),
    #         Column("guild_id", Integer),
    #     )
    #     metadata.create_all(engine)

    Base.metadata.create_all(engine)


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
