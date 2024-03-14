# Upload a submission as part of the specified Purdue Plays challenge
from utils.constants import SERVERS, Session, bot
from discord.ext import commands
from utils.messages import NO_GUILD_ERROR, NOT_IMPLEMENTED_ERROR


@bot.slash_command(
    name="upload_purdue_plays",
    description="Upload a submission to the specified Purdue Plays challenge",
    guild_ids=SERVERS,
)
async def get_purdue_plays(ctx, challenge_name) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
