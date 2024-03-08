from typing import List
from discord import VoiceClient
from discord.ext import commands
from src.slash_commands.add_to_playlist import SUCCESS_MESSAGE
from utils.constants import DB_CLIENT, SERVERS, PlaylistNames, bot, ydl

# from utils.state import CURRENT_SONG
from models.songs import Song
from youtube_service import sync_playlist

CURRENT_SONG_MESSAGE = "Blowbot is not currently playing anything"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
GENERIC_ERROR = "An error occurred while syncing the playlist"
SUCCESS_MESSAGE = "Playlist synced"


@bot.command(
    name="sync_playlist",
    description="Syncs the playlist with the YT playlist if you are an admin, REMOVES RANDOMIZATION",
    guild_ids=SERVERS,
)
async def sync_playlist_command(ctx: commands.Context, playlist_name: str) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    try:
        if playlist_name in PlaylistNames:
            await sync_playlist(db, ydl, PlaylistNames.from_string(playlist_name))
            await ctx.send(SUCCESS_MESSAGE)
    except Exception as e:
        await ctx.send(GENERIC_ERROR)
