# Get information about current Purdue Plays challenges
from utils.constants import SERVERS, Session, bot
from discord.ext import commands
from utils.messages import NO_GUILD_ERROR, NOT_IMPLEMENTED_ERROR


@bot.slash_command(
    name="get_purdue_plays",
    description="Get information about current Purdue Plays challenges",
    guild_ids=SERVERS,
)
async def get_purdue_plays(ctx) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
