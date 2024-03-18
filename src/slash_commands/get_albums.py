# Retrieve albums that match the specified parameters
from models.model_fields import AlbumFields
from utils.constants import SERVERS, Session, bot, yt
from services import discord_service
from utils.messages import (
    ADMIN_ONLY_ERROR,
    CONNECTION_ERROR,
    NO_GUILD_ERROR,
    NOT_IMPLEMENTED_ERROR,
)


@bot.slash_command(
    name="get_albums",
    description="Retrieve a list of albums that match the specified parameters",
    guild_ids=SERVERS,
)
async def get_albums(
    ctx,
    id: int | None,
    name: str | None,
    completed: bool | None,
    track_name: str | None,
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        if discord_service.is_admin(ctx.author):  # type: ignore
            await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
            return
        else:
            await ctx.respond(ADMIN_ONLY_ERROR.format("get_albums"), ephemeral=True)
            return
