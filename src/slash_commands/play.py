from typing import Any
from discord.ext import commands
from utils.constants import DB_CLIENT, SERVERS, bot
from services import discord_service


SUCCESS_MESSAGE = "Blowbot was resumed by {ctx.author.name}"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.command(
    name="play",
    description="Attempt to resume blowbot playback",
    guild_ids=SERVERS,
)
async def play(ctx: commands.Context) -> Any:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # play the current song
    await discord_service.play_song()
    # return a success message as confirmation
    await ctx.send(SUCCESS_MESSAGE, ephemeral=True)
    return
