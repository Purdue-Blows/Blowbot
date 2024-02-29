from utils.constants import (
    BOT_DEBUGGING_SERVER_CHANNEL_IDS,
    DISCORD_TOKEN,
    SERVERS,
    PURDUE_BLOWS_CHANNEL_IDS,
    PURDUE_BLOWS_PLAYLIST_URL,
    bot,
)

# Register commands
from commands import (
    add_to_playlist,
    add_to_queue,
    get_current_song,
    get_playlist,
    help,
    jazz_trivia,
    jazzle,
    profile,
    remove_from_playlist,
    remove_from_queue,
    view_queue,
)

# Register events
from events import welcome
from utils.functions import is_bot_playing, clear_queue


# Start playing from the playlist on_ready
@bot.event
async def on_ready():
    # Check if the bot is currently playing music
    if not await is_bot_playing():
        # Get the voice channel to join
        voice_channel = bot.get_channel(
            BOT_DEBUGGING_SERVER_CHANNEL_IDS["general_voice"]
        )

        # Check if the bot is already in a voice channel
        if bot.voice_client is not None:
            await bot.voice_client.move_to(voice_channel)
        else:
            # Connect the bot to the voice channel
            await voice_channel.connect()

        # Start streaming from the playlist


@bot.event
async def on_disconnect():
    # Clear the queue
    await clear_queue()


bot.run(DISCORD_TOKEN)
