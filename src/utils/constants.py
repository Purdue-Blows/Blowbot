import os
from dotenv import load_dotenv

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
