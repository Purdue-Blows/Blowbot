from typing import List, Optional
from discord.ext import commands
from models.playback import Playback
from src.models.playlist import Playlist
from utils.constants import (
    DB_CLIENT,
    PURDUE_BLOWS_PLAYLISTS,
    SERVERS,
    PlaylistNames,
    bot,
)

NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
GENERIC_ERROR = "Playlist could not be shuffled"
SUCCESS_MESSAGE = "Playlist shuffled"
INVALID_PLAYLIST_NAME = "Invalid playlist name"


@bot.command(
    name="shuffle_playlist",
    description="Shuffles the currently unplayed songs of the currently playing playlist",
    # TODO: come back to this and look into autocomplete options
    # options=[
    #     commands.Option(
    #         name="playlist_name",
    #         description="The name of the playlist to shuffle",
    #         type=commands.OptionType.STRING,
    #         required=False,
    #         choices=[
    #         commands.OptionChoice(name=name.value, value=name.value)
    #         for name in PlaylistName
    #         ],
    #     )
    #     ],
    guild_ids=SERVERS,
)
async def shuffle_playlist(ctx: commands.Context, playlist_name: Optional[str]) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # Shuffles the currently unplayed songs of the currently playing playlist
    try:
        if playlist_name in PlaylistNames:
            shuffle = await Playlist.shuffle(
                db, PlaylistNames.from_string(playlist_name)
            )
            if shuffle:
                await ctx.send(SUCCESS_MESSAGE, ephemeral=True)
            else:
                await ctx.send(GENERIC_ERROR, ephemeral=True)
        else:
            await ctx.send(INVALID_PLAYLIST_NAME, ephemeral=True)
    except Exception:
        await ctx.send(GENERIC_ERROR, ephemeral=True)
