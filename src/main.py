import asyncio
from http import client
from math import e
from os import name
import discord
from discord.ext import commands

from utils.constants import (
    BOT_DEBUGGING_SERVER_CHANNEL_IDS,
    BOT_DEBUGGING_SERVER_ID,
    DISCORD_TOKEN,
    PURDUE_BLOWS_SERVER_ID,
    SERVERS,
    PURDUE_BLOWS_CHANNEL_IDS,
    PlaylistNames,
    Session,
    bot,
    ydl,
    initialize_collections,
    engine,
)

# For discord audio
import nacl

# Register commands
from slash_commands import (
    add_to_playlist,
    add_to_queue,
    back,
    clear_queue,
    create_purdue_plays,
    edit_playlist_song,
    get_current_song,
    get_playlist,
    get_purdue_plays,
    # help,
    jazz_trivia,
    jazzle,
    pause,
    play,
    profile,
    remove_from_playlist,
    remove_from_queue,
    shuffle_playlist,
    skip,
    switch_playlist,
    sync_playlist,
    upload_purdue_plays,
    view_queue,
)

# Register events
from events import song_over, welcome
from events.song_over import on_song_over, on_track_end

from services.discord_service import (
    is_bot_playing,
    is_bot_connected,
    disconnect,
    move_to,
    play_song,
)
from models.songs import Song
from models.users import User
from models.playlist import Playlist
from models.queue import Queue
from models.playback import Playback

from services.youtube_service import sync_playlist

VOICE_CONNECT_ERROR_MESSAGE = "Could not connect to voice"


# Start playing from the playlist on_ready
@bot.event
async def on_ready():
    # Initialize databases
    await initialize_collections(engine)
    # Sync command tree
    # await bot.sync_commands()
    with Session() as session:
        # TODO: just test code rn
        # for playlist_name in PlaylistNames:
        #     await sync_playlist(
        #         session, BOT_DEBUGGING_SERVER_ID, ydl, playlist_name=playlist_name
        #     )

        guild = bot.get_guild(BOT_DEBUGGING_SERVER_ID)
        assert guild != None
        channel: discord.VoiceChannel = guild.get_channel(BOT_DEBUGGING_SERVER_CHANNEL_IDS["general_voice"])  # type: ignore
        assert channel != None
        # Check if the bot is currently playing music
        if not await is_bot_playing(bot):
            # Get the voice channel to join
            voice_client = await move_to(channel)
            if voice_client == None:
                raise Exception(VOICE_CONNECT_ERROR_MESSAGE)
            print("Started")
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
            # NOTE: in order for blowbot to actually play a song
            # NOTE: this is all test code
            # try:
            #     print("Shuffle")
            #     await Playlist.shuffle(
            #         session,
            #         BOT_DEBUGGING_SERVER_ID,
            #         playlist_name=PlaylistNames.COMMUNITY,
            #     )
            #     print("Playlist retrieval")
            #     playlist = await Playlist.retrieve_one(
            #         session,
            #         BOT_DEBUGGING_SERVER_ID,
            #         playlist_name=PlaylistNames.COMMUNITY.value,
            #         song_id=1,
            #     )
            #     if playlist != None:
            #         print(playlist.to_string())
            #         song = await Song.retrieve_one(session, id=playlist.song.id)
            #         print(song.to_string())
            #         if not song:
            #             raise Exception("Audio is None")
            #         if song.audio is None:
            #             raise Exception("Audio is None")
            #         await play_song(bot, song.audio)  # type: ignore
            #         print("Streaming!")
            #     else:
            #         print("Playlist is: None")
            # except Exception as e:
            #     print(e)
            #     return


@bot.event
async def on_disconnect():
    # Clear playback and queues for all servers
    with Session() as session:
        queue_guild_ids = session.query(Queue.guild_id).distinct().all()
        guild_ids = [guild_id for (guild_id,) in queue_guild_ids]
        for guild_id in guild_ids:
            # This might not be very fault tolerant design,
            # but at the very least it does force us to get it right
            await Queue.clear_queue(session, guild_id)
            await Playback.delete(session, guild_id)

    # Disconnect from vc; unnecessary, bot handles automatically
    # if await is_bot_connected(bot):
    #     await disconnect(bot)


try:
    bot.run(DISCORD_TOKEN)  # type: ignore
except KeyboardInterrupt:
    # Clear the queue
    asyncio.run(on_disconnect())
    # stop_db()
