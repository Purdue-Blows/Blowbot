import os
import discord
import sqlite3
from dotenv import load_dotenv
from discord.ext import commands

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if not load_dotenv(os.path.join(BASE_DIR, ".env")):
    raise Exception("Could not parse the .env file")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID: int = int(os.getenv("CLIENT_ID"))  # type: ignore
PURDUE_BLOWS_SERVER_ID: int = int(os.getenv("PURDUE_BLOWS_SERVER_ID"))  # type: ignore
BOT_DEBUGGING_SERVER_ID: int = int(os.getenv("BOT_DEBUGGING_SERVER_ID"))  # type: ignore
SERVERS = [PURDUE_BLOWS_SERVER_ID, BOT_DEBUGGING_SERVER_ID]
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")
SPOTIFY_ID = os.getenv("SPOTIFY_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
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
PURDUE_BLOWS_PLAYLIST_URL = (
    "https://www.youtube.com/playlist?list=PLDLRACxotfNFS5nL608HiV84mN0RkUpUY"
)

DB = "blowbot.db"

intents = discord.Intents.default() | discord.Intents.members

# Initialize bot
bot = commands.Bot(intents=intents)
assert bot != None

# Initialize spotify
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRET
    )
)
assert spotify != None

# Initialize database, creating tables if the db doesn't exist
con = None
if not os.path.exists(os.path.join(BASE_DIR, DB)):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        """
        CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, jazzle_streak INTEGER, 
        jazz_trivia_correct INTEGER, jazz_trivia_incorrect INTEGER, 
        jazz_trivia_percentage REAL)
        """
    )
    cur.execute(
        """
        CREATE TABLE songs(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, artist TEXT, url TEXT UNIQUE, album TEXT NULL, 
        release_date TEXT NULL)
        """
    )
    cur.execute(
        """
        CREATE TABLE playlist(id INTEGER PRIMARY KEY AUTOINCREMENT, song_id INTEGER, song BLOB, played BOOLEAN, user_id INTEGER,
        FOREIGN KEY(song_id) REFERENCES songs(id))
        """
    )
    cur.execute(
        """
        CREATE TABLE queue(id INTEGER PRIMARY KEY AUTOINCREMENT, song_id INTEGER, song BLOB, user_id INTEGER,
        FOREIGN KEY(song_id) REFERENCES songs(id))
        """
    )
    cur.execute("PRAGMA foreign_keys = ON")
else:
    con = sqlite3.connect(DB)
assert con != None

# Initialize yt-dlp
yt_opts = {
    "best-audio": True,
    "extract_audio": True,
    "noplaylist": True,
    "audio-format": "mp3",
    "audio-quality": 0,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        },
    ],
}
ydl = yt_dlp.YoutubeDL(yt_opts)
assert ydl != None
