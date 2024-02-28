from utils.constants import (
    BOT_DEBUGGING_SERVER_CHANNEL_IDS,
    DISCORD_TOKEN,
    SERVERS,
    bot,
    spotify
)

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

# Start playing from the playlist on_ready
@bot.event
async def on_ready():
    # Check if bot is currently streaming the Purdue Blows playlist
    spotify.
    # If not, start streaming

bot.run(DISCORD_TOKEN)
