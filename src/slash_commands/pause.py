from typing import Any
from discord.ext import commands
from utils.constants import DB_CLIENT, SERVERS, bot
from services import discord_service


PAUSE_MESSAGE = "Blowbot was paused by {ctx.author.name}"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.command(
    name="pause",
    description="Pause Blowbot",
    guild_ids=SERVERS,
)
async def pause(ctx: commands.Context) -> Any:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # pause the current song
    await discord_service.pause()
    # return a success message as confirmation
    await ctx.send(PAUSE_MESSAGE, ephemeral=True)
    return
