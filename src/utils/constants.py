import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyOAuth

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if not load_dotenv(os.path.join(BASE_DIR, ".env")):
    raise Exception("Could not parse the .env file")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
PURDUE_BLOWS_SERVER_ID = os.getenv("PURDUE_BLOWS_SERVER_ID")
BOT_DEBUGGING_SERVER_ID = os.getenv("BOT_DEBUGGING_SERVER_ID")
SERVERS = [PURDUE_BLOWS_SERVER_ID, BOT_DEBUGGING_SERVER_ID]
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")
SPOTIFY_ID = os.getenv("SPOTIFY_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")

PURDUE_BLOWS_CHANNEL_IDS = {
    "general": "1148646209586745391",
    "commands": "1210003092356210779",
    "vibe": "1212457675087024148",
}

BOT_DEBUGGING_SERVER_CHANNEL_IDS = {
    "general": "909075276774907947",
    "general_voice": "909075276774907948",
}

PURDUE_BLOWS_PLAYLIST_URL = "https://open.spotify.com/playlist/6MPc4BFOUT9mUIz0G6ME4B?si=z4XGO1ELRLqfS3TyrmbiHA&pt_success=1&nd=1&dlsi=11e24dc164584f44"


intents = discord.Intents.default() | discord.Intents.members

# Initialize bot
bot = commands.Bot(intents=intents)

# Initialize spotify client
# Note that only admins can use some spotify commands
scope = "user-modify-playback-state"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
