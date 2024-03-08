from typing import List
from discord.ext import commands
from src.models.playlist import Playlist
from src.slash_commands.add_to_playlist import SUCCESS_MESSAGE
from utils.constants import (
    DB_CLIENT,
    PURDUE_BLOWS_PLAYLISTS,
    SERVERS,
    PlaylistNames,
    bot,
)

NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
SUCCESS_MESSAGE = "Playlist switched"
GENERIC_ERROR = "Playlist could not be switched"


@bot.command(
    name="switch_playlist",
    description="Switch the currently playing playlist",
    guild_ids=SERVERS,
)
async def switch_playlist(ctx: commands.Context, new_playlist_name: str) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # Switch the currently playing playlist
    try:
        if new_playlist_name in PlaylistNames:
            await Playlist.switch_playlist(
                db, PlaylistNames.from_string(new_playlist_name)
            )
            await ctx.send(SUCCESS_MESSAGE, ephemeral=True)
        else:
            await ctx.send("Invalid playlist name", ephemeral=True)
    except Exception:
        await ctx.send(GENERIC_ERROR, ephemeral=True)
