from typing import Any
from discord.ext import commands
from utils.constants import SERVERS, Session, bot
from utils.messages import NO_GUILD_ERROR, NOT_IMPLEMENTED_ERROR


@bot.slash_command(
    name="jazz_trivia",
    description="Get a jazz trivia question, see your jazz trivia stats",
    guild_ids=SERVERS,
)
async def jazz_trivia(ctx) -> Any:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
