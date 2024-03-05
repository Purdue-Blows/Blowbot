from typing import Any
from discord.ext import commands
from utils.constants import SERVERS, bot
from services import discord


PAUSE_MESSAGE = "Blowbot was paused by {ctx.author.name}"


@bot.slash_command(
    name="pause",
    description="Pause Blowbot",
    guild_ids=SERVERS,
)
async def pause(ctx: commands.Context) -> Any:
    # pause the current song
    await discord.pause()
    # return a success message as confirmation
    await ctx.respond(PAUSE_MESSAGE, ephemeral=True)
    return
