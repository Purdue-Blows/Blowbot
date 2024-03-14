# Create a Purdue Plays challenges; currently admin only
from typing import Optional
from utils.constants import SERVERS, Session, bot
from discord.ext import commands
from utils.messages import ADMIN_ONLY_ERROR, NO_GUILD_ERROR, NOT_IMPLEMENTED_ERROR
from services import discord_service


@bot.slash_command(
    name="edit_playlist_song",
    description="Edit the data for a song in the playlist",
    guild_ids=SERVERS,
)
async def edit_playlist_song(
    ctx,
    name: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    release_date: Optional[str] = None,
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        if discord_service.is_admin(ctx.author):  # type: ignore
            await ctx.respond(NOT_IMPLEMENTED_ERROR, ephemeral=True)
            return
        else:
            await ctx.respond(
                ADMIN_ONLY_ERROR.format("edit_playlist_song"), ephemeral=True
            )
            return
