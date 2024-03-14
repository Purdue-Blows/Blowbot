import traceback
import discord
from discord.ext import commands
from models.playlist import Playlist
from slash_commands.add_to_playlist import SUCCESS_MESSAGE
from utils.constants import (
    PURDUE_BLOWS_PLAYLISTS,
    SERVERS,
    PlaylistNames,
    Session,
    bot,
)
from utils.messages import GENERIC_ERROR, NO_GUILD_ERROR


SUCCESS_MESSAGE = "Playlist switched"


@bot.slash_command(
    name="switch_playlist",
    description="Switch the currently playing playlist",
    guild_ids=SERVERS,
)
async def switch_playlist(
    ctx,
    new_playlist_name: discord.Option(
        str,
        choices=[PlaylistNames.value for PlaylistNames in PlaylistNames],
        description="The name of the playlist",
    ),  # type: ignore
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # Switch the currently playing playlist
        try:
            if new_playlist_name in PlaylistNames:
                await Playlist.switch_playlist(
                    session,
                    ctx.guild.id,
                    PlaylistNames.from_string(new_playlist_name.value),
                )
                await ctx.respond(SUCCESS_MESSAGE, ephemeral=True)
            else:
                await ctx.respond("Invalid playlist name", ephemeral=True)
        except Exception:
            await ctx.respond(GENERIC_ERROR.format("switch_playlist"), ephemeral=True)
            traceback.print_exc()
