from typing import Union
from utils.state import CURRENT_SONG
from utils.constants import bot
import pycord.discord as discord
from discord.Member import Member
from discord.User import User
from models.playlist import Playlist
from models.queue import Queue


# Checks if the bot is currently playing a song
async def is_bot_playing() -> bool:
    return CURRENT_SONG is not None


# Checks if the bot is connected to a VC
async def is_bot_connected() -> bool:
    return bot.voice_client is not None


# Attempts to connect the song to a VC vc
async def connect(vc: discord.VoiceClient) -> None:
    bot.voice_client = vc
    return


# Attempts to connect the song to a VC vc
async def move_to(vc: discord.VoiceClient) -> None:
    bot.voice_client.move_to(vc)
    return


# Attempts to disconnect the bot from voice
async def disconnect() -> None:
    bot.voice_client = None
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
        bot.voice_client.play(CURRENT_SONG.audio)


# Pause the current song
async def pause() -> None:
    global CURRENT_SONG
    if (
        CURRENT_SONG is not None
        and (isinstance(CURRENT_SONG, Playlist) or isinstance(CURRENT_SONG, Queue))
        and CURRENT_SONG.audio is not None
    ):
        bot.voice_client.pause(CURRENT_SONG.audio)
