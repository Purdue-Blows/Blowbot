from typing import Any
from discord.ext import commands
from src.models.playback import Playback
from src.models.playlist import Playlist
from utils.constants import DB_CLIENT, SERVERS, bot
from services import discord_service


PAUSE_MESSAGE = "Blowbot was paused by {ctx.author.name}"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
GENERIC_ERROR = "There was an error trying to pause"


@bot.command(
    name="pause",
    description="Pause Blowbot",
    guild_ids=SERVERS,
)
async def pause(ctx: commands.Context) -> Any:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    try:
        db = DB_CLIENT[str(ctx.guild.id)]
        # pause the current song
        await discord_service.pause(bot)
        # return a success message as confirmation
        await ctx.send(PAUSE_MESSAGE, ephemeral=True)
        return
    except Exception:
        await ctx.send(GENERIC_ERROR, ephemeral=True)
        return
