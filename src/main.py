from discord.ext import commands
from utils.constants import BOT_DEBUGGING_SERVER_CHANNEL_IDS, DISCORD_TOKEN, SERVERS

# Initialize bot
from bot import bot

# Register commands
from commands import (
    add_to_playlist,
    get_current_song,
    get_playlist,
    help,
    jazz_trivia,
    jazzle,
    play_song,
    profile,
    remove_from_playlist,
    remove_from_queue,
    view_queue,
)

# Register events
from events import welcome

bot.run(DISCORD_TOKEN)
