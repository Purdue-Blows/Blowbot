# Create a Purdue Plays challenges; currently admin only
from utils.constants import SERVERS, Session, bot, yt
from services import discord_service
from utils.messages import (
    ADMIN_ONLY_ERROR,
    CONNECTION_ERROR,
    NO_GUILD_ERROR,
    NOT_IMPLEMENTED_ERROR,
)


@bot.slash_command(
    name="create_purdue_plays",
    description="Creates a new Purdue Plays challenge (if you are an admin)",
    guild_ids=SERVERS,
)
async def create_purdue_plays(ctx, todo) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    if yt.refresh_token == None:
        await ctx.respond(
            CONNECTION_ERROR.format(
                "YouTube", "the current refresh token is invalid or has expired"
            ),
            ephemeral=True,
        )
        return
    with Session() as session:
        if discord_service.is_admin(ctx.author):  # type: ignore
            await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
            return
        else:
            await ctx.respond(
                ADMIN_ONLY_ERROR.format("create_purdue_plays"), ephemeral=True
            )
            return
