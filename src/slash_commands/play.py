from typing import Any
from discord.ext import commands
from utils.constants import SERVERS, bot
from services import discord


SUCCESS_MESSAGE = "Blowbot was resumed by {ctx.author.name}"


@bot.slash_command(
    name="play",
    description="Attempt to resume blowbot playback",
    guild_ids=SERVERS,
)
async def play(ctx: commands.Context) -> Any:
    # pause the current song
    await discord.play_song()
    # return a success message as confirmation
    await ctx.respond(SUCCESS_MESSAGE, ephemeral=True)
    return
