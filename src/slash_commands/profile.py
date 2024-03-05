from typing import Any
from discord.ext import commands
from utils.constants import SERVERS, bot


RESPONSE_MESSAGE = "Sorry, this command hasn't been implemented yet!"


@bot.slash_command(
    name="profile",
    description="Get information about your current user profile",
    guild_ids=SERVERS,
)
async def profile(ctx: commands.Context) -> Any:
    await ctx.respond(RESPONSE_MESSAGE, ephemeral=True)
