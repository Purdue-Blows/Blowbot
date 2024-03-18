# Update a track from an album
from discord import File
from models.model_fields import AlbumFields
from utils.constants import SERVERS, Session, bot, yt
from services import discord_service
from utils.messages import (
    ADMIN_ONLY_ERROR,
    CONNECTION_ERROR,
    MORE_DATA_ERROR,
    NO_GUILD_ERROR,
    NOT_IMPLEMENTED_ERROR,
)


@bot.slash_command(
    name="update_album_track",
    description="Update a track from an album (only if you've accepted it)",
    guild_ids=SERVERS,
)
async def update_album_track(
    ctx,
    id: int | None,
    name: str | None,
    description: str | None,
    score: File | None,
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # Check if id or name is specified
        if id is None and name is None:
            ctx.respond(MORE_DATA_ERROR.format("id or name"), ephemeral=True)
            return
        # TODO: Check if user is in role
        # TODO: plan and implement rest
