from typing import Any
from discord.ext import commands
from utils.constants import SERVERS, bot
from services import discord


@bot.slash_command(
    name="pause",
    description="Pause Blowbot",
    guild_ids=SERVERS,
)
async def pause(ctx: commands.Context) -> Any:
    # pause the current song
    await discord.pause()
    # return a success message as confirmation
    await ctx.respond(f"Blowbot was paused by {ctx.author.name}", ephemeral=True)
    return
