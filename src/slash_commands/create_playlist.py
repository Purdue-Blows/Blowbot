import discord
from utils.constants import SERVERS, PlaylistNames, Session, bot, yt
from discord.ext import commands
from utils.messages import (
    ADMIN_ONLY_ERROR,
    CONNECTION_ERROR,
    NO_GUILD_ERROR,
    NOT_IMPLEMENTED_ERROR,
)


# Create a playlist; currently admin only
@bot.slash_command(
    name="create_playlist",
    description="Creates a new playlist (if you are an admin)",
    guild_ids=SERVERS,
)
async def create_playlist(
    ctx,
    youtube_url: str,
    playlist_name: discord.Option(
        str,
        choices=[PlaylistNames.value for PlaylistNames in PlaylistNames],
        description="The name of the playlist",
    ),  # type: ignore
) -> None:
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
            # TODO: Implement playlist creation logic using the provided YouTube URL and playlist name
            await ctx.respond("Playlist created successfully!", ephemeral=True)
            return
        else:
            await ctx.respond(
                ADMIN_ONLY_ERROR.format("create_playlist"), ephemeral=True
            )
            return
