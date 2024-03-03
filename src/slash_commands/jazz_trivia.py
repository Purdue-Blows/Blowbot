from typing import Any
from discord.ext import commands
from utils.constants import SERVERS, bot


@bot.slash_command(
    name="jazz_trivia",
    description="Get a jazz trivia question, see your jazz trivia stats",
    guild_ids=SERVERS,
)
async def jazz_trivia(ctx: commands.Context) -> Any:
    await ctx.respond(
        "Sorry, this command hasn't been implemented yet!", ephemeral=True
    )
