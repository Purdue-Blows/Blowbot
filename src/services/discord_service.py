from typing import Union
from models.songs import Song

# from utils.constants import bot
from discord.ext.commands import Bot

# from discord import VoiceChannel
from discord import Member, VoiceChannel, VoiceClient, VoiceProtocol, AudioSource
import discord
import io
from models.playlist import Playlist
from models.queue import Queue


# Checks if the bot is currently playing a song
async def is_bot_playing(bot: Bot) -> bool:
    for vc in bot.voice_clients:
        if vc:
            return True
    return False


# Checks if the bot is connected to a VC
async def is_bot_connected(bot: Bot) -> bool:
    return len(bot.voice_clients) != 0


# Attempts to connect the song to a VC vc
# async def connect(channel: VoiceChannel) -> None:
#     await channel.connect()  # type: ignore
#     return


# Attempts to connect the song to a VC vc
async def move_to(channel: VoiceChannel) -> VoiceClient | None:
    client: VoiceClient = await channel.connect()
    if client:
        return client
    else:
        return None


# Attempts to disconnect the bot from voice
async def disconnect(bot: Bot) -> None:
    for vc in bot.voice_clients:
        await vc.disconnect(force=True)
    return


# Check if the account in question is an admin in the server
async def is_admin(account: Member) -> bool:
    return account.guild_permissions.administrator


# Play the current song
async def play_song(bot: Bot, audio: bytes) -> None:
    if await is_bot_playing(bot):
        raise Exception("Bot is already playing")
    if await is_bot_connected(bot):
        for vc in bot.voice_clients:
            if vc:
                if isinstance(vc, VoiceClient):
                    vc.play(discord.FFmpegPCMAudio(io.BytesIO(audio)))
    return


# Pause the current song
async def pause(bot: Bot) -> None:
    if await is_bot_playing(bot):
        raise Exception("Bot is not currently playing")
    if await is_bot_connected(bot):
        for vc in bot.voice_clients:
            if vc:
                if isinstance(vc, VoiceClient):
                    vc.pause()
    return
