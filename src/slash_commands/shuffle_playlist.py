import traceback
from typing import List, Optional
import discord
from discord.ext import commands
from models.playback import Playback
from models.playlist import Playlist
from utils.constants import (
    PURDUE_BLOWS_PLAYLISTS,
    SERVERS,
    PlaylistNames,
    Session,
    bot,
)
from utils.messages import GENERIC_ERROR, NO_GUILD_ERROR


SUCCESS_MESSAGE = "Playlist shuffled"
INVALID_PLAYLIST_NAME = "Invalid playlist name"


@bot.slash_command(
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
async def shuffle_playlist(
    ctx,
    playlist_name: discord.Option(
        str,
        choices=[PlaylistNames.value for PlaylistNames in PlaylistNames],
        description="The name of the playlist",
        required=False,
    ),  # type: ignore
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # Shuffles the currently unplayed songs of the currently playing playlist
        try:
            if playlist_name in PlaylistNames:
                shuffle = await Playlist.shuffle(
                    session,
                    ctx.guild.id,
                    PlaylistNames.from_string(
                        playlist_name.value,  # type: ignore
                    ),
                )
                if shuffle:
                    await ctx.send(SUCCESS_MESSAGE)
                    return
                else:
                    await ctx.respond(
                        GENERIC_ERROR.format("shuffle_playlist"), ephemeral=True
                    )
                    return
            else:
                await ctx.respond(INVALID_PLAYLIST_NAME, ephemeral=True)
        except Exception:
            await ctx.respond(GENERIC_ERROR.format("shuffle_playlist"), ephemeral=True)
            traceback.print_exc()
