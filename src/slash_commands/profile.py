from typing import Any
from discord.ext import commands
from utils.constants import DB_CLIENT, SERVERS, bot


RESPONSE_MESSAGE = "Sorry, this command hasn't been implemented yet!"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.command(
    name="profile",
    description="Get information about your current user profile",
    guild_ids=SERVERS,
)
async def profile(ctx: commands.Context) -> Any:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    await ctx.send(RESPONSE_MESSAGE, ephemeral=True)
