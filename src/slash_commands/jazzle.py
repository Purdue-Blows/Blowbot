from typing import Any

# from discord.ext import commands

from utils.messages import NO_GUILD_ERROR, NOT_IMPLEMENTED_ERROR

from utils.constants import SERVERS, Session, bot


@bot.command(
    name="jazzle",
    description="Determine the jazz standard based on a number of hints. How many tries can you get it in?",
    guild_ids=SERVERS,
)
async def jazzle(ctx) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
