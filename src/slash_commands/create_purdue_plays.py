# Create a Purdue Plays challenges; currently admin only
from utils.constants import SERVERS, Session, bot
from discord.ext import commands
from utils.messages import ADMIN_ONLY_ERROR, NO_GUILD_ERROR, NOT_IMPLEMENTED_ERROR


@bot.slash_command(
    name="create_purdue_plays",
    description="Creates a new Purdue Plays challenge (if you are an admin)",
    guild_ids=SERVERS,
)
async def create_purdue_plays(ctx, todo) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        if discord_service.is_admin(ctx.author):  # type: ignore
            await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
            return
        else:
            await ctx.respond(
                ADMIN_ONLY_ERROR.format("create_purdue_plays"), ephemeral=True
            )
            return
