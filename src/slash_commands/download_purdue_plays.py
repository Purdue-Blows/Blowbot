# An editor/admin-only command; allows a user to download all of the current submissions of a purdue plays challenge
from utils.constants import SERVERS, RoleNames, Session, bot, yt
from services import discord_service
from utils.messages import (
    CONNECTION_ERROR,
    NO_GUILD_ERROR,
    NOT_IMPLEMENTED_ERROR,
    ROLE_ERROR,
)


@bot.slash_command(
    name="download_purdue_plays",
    description="Download submissions to a Purdue Plays challenge (if you are an editor/admin)",
    guild_ids=SERVERS,
)
async def download_purdue_plays(ctx, todo) -> None:
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
        if discord_service.is_admin(ctx.author) or discord_service.has_role(
            ctx.author,
            [
                role
                for role in await discord_service.get_roles(ctx.guild)
                if role.name == RoleNames.EDITOR.value
            ][0],
        ):  # type: ignore
            await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
            return
        else:
            await ctx.respond(
                ROLE_ERROR.format("download_purdue_plays", "admin, editor"),
                ephemeral=True,
            )
            return
