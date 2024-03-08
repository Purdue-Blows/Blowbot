import asyncio
from http import client
from math import e
from os import name
from models.playlist import Playlist
from models.songs import Song
from utils.constants import (
    BOT_DEBUGGING_SERVER_CHANNEL_IDS,
    BOT_DEBUGGING_SERVER_ID,
    DISCORD_TOKEN,
    MONGO_HOST,
    MONGO_PORT,
    SERVERS,
    PURDUE_BLOWS_CHANNEL_IDS,
    PlaylistNames,
    bot,
    ydl,
    DB_CLIENT,
    initialize_collections,
    mongod,
)

# For discord audio
import nacl

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
from services.discord_service import (
    is_bot_playing,
    is_bot_connected,
    disconnect,
    move_to,
    play_song,
)
from models.queue import Queue
import discord

from services.youtube_service import sync_playlist

VOICE_CONNECT_ERROR_MESSAGE = "Could not connect to voice"


# Start playing from the playlist on_ready
@bot.event
async def on_ready():
    # Initialize databases
    for server in SERVERS:
        db = DB_CLIENT[str(server)]
        await initialize_collections(db)
        for playlist_name in PlaylistNames:
            await sync_playlist(db, ydl, playlist_name=playlist_name)
    print("Collections initialized")

    guild = bot.get_guild(BOT_DEBUGGING_SERVER_ID)
    assert guild != None
    channel: discord.VoiceChannel = guild.get_channel(BOT_DEBUGGING_SERVER_CHANNEL_IDS["general_voice"])  # type: ignore
    assert channel != None
    # Check if the bot is currently playing music
    if not await is_bot_playing(bot):
        # Get the voice channel to join
        voice_client = await move_to(channel)
        if DB_CLIENT == None:
            raise Exception(VOICE_CONNECT_ERROR_MESSAGE)
        # Sync playlist if not synced
        # await sync_playlist()
        # print("Attempting to add a test song")
        # await Song.add(
        #     Song(
        #         name="test",
        #         artist="test",
        #         url="test",
        #         album="test",
        #         release_date="test",
        #     )
        # )
        print("Playlist synced")
        # NOTE: in order for blowbot to actually play a song
        # try:
        #     await Playlist.shuffle(db)
        #     playlist = await Playlist.retrieve_one(db)
        #     if playlist != None:
        #         song = await Song.retrieve_one(id=playlist.song.id)
        #         if not song:
        #             raise Exception("Audio is None")
        #         if song.audio is None:
        #             raise Exception("Audio is None")
        #         await play_song(bot, song.audio)
        #         print("Streaming!")
        # except Exception as e:
        #     return


@bot.event
async def on_disconnect():
    # Clear the queue for all servers
    for server in SERVERS:
        db = DB_CLIENT[str(server)]
        await Queue.clear_queue(db)

    # Cleanly shutdown the db
    DB_CLIENT.close()
    mongod.kill()

    # Disconnect from vc
    if await is_bot_connected(bot):
        await disconnect(bot)


try:
    bot.run(DISCORD_TOKEN)  # type: ignore
except KeyboardInterrupt:
    print("Should be shutting down mongod")
    # Clear the queue
    asyncio.run(on_disconnect())
