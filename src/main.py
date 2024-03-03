from dis import disco
from tkinter import CURRENT
from models.playlist import Playlist
from slash_commands.play import play
from utils.constants import (
    BOT_DEBUGGING_SERVER_CHANNEL_IDS,
    DISCORD_TOKEN,
    SERVERS,
    PURDUE_BLOWS_CHANNEL_IDS,
    PURDUE_BLOWS_PLAYLIST_URL,
    bot,
)

# Register commands
from slash_commands import (
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
from services.discord import (
    is_bot_playing,
    is_bot_connected,
    connect,
    disconnect,
    move_to,
    play_song,
)
from models.queue import Queue
from utils.state import CURRENT_SONG


# Start playing from the playlist on_ready
@bot.event
async def on_ready():
    global CURRENT_SONG
    # Check if the bot is currently playing music
    if not await is_bot_playing():
        # Get the voice channel to join
        if not await is_bot_connected():
            await connect(BOT_DEBUGGING_SERVER_CHANNEL_IDS["general_voice"])
        else:
            await move_to(BOT_DEBUGGING_SERVER_CHANNEL_IDS["general_voice"])

        # Initialize the current song
        CURRENT_SONG = await Playlist.retrieve_one()

        # Start streaming from the playlist
        await play_song()


@bot.event
async def on_disconnect():
    # Clear the queue
    await Queue.clear_queue()

    # Disconnect from vc
    if await is_bot_connected():
        await disconnect()


bot.run(DISCORD_TOKEN)
