from typing import Union
from utils.state import CURRENT_SONG
from utils.constants import bot
from discord import VoiceChannel
from discord import Member
from discord import User
from models.playlist import Playlist
from models.queue import Queue


# Checks if the bot is currently playing a song
async def is_bot_playing() -> bool:
    return CURRENT_SONG is not None


# Checks if the bot is connected to a VC
async def is_bot_connected() -> bool:
    return bot.voice_clients is not None


# Attempts to connect the song to a VC vc
async def connect(id: str) -> None:
    vc = bot.get_channel(id)
    print(vc)
    vc.connect()
    # bot.voice_clients = vc
    return


# Attempts to connect the song to a VC vc
async def move_to(id: str) -> None:
    vc = bot.get_channel(id)
    print(vc)
    vc.connect()
    # bot.voice_clients.move_to(vc)
    return


# Attempts to disconnect the bot from voice
async def disconnect() -> None:
    for vc in bot.voice_clients:
        vc.disconnect()
    return


# Check if the account in question is an admin in the server
async def is_admin(account: Union[User, Member]) -> bool:
    return account.guild_permissions.administrator


# Play the current song
async def play_song() -> None:
    global CURRENT_SONG
    if (
        CURRENT_SONG is not None
        and (isinstance(CURRENT_SONG, Playlist) or isinstance(CURRENT_SONG, Queue))
        and CURRENT_SONG.audio is not None
    ):
        bot.voice_clients.play(CURRENT_SONG.audio)


# Pause the current song
async def pause() -> None:
    global CURRENT_SONG
    if (
        CURRENT_SONG is not None
        and (isinstance(CURRENT_SONG, Playlist) or isinstance(CURRENT_SONG, Queue))
        and CURRENT_SONG.audio is not None
    ):
        bot.voice_clients.pause(CURRENT_SONG.audio)
