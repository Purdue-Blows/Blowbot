from math import e
from commands.play import play
from models.playlist import Playlist
from models.songs import Song
from utils.constants import SERVERS, bot
from services import youtube
from discord.ext import commands
from typing import Any


@bot.slash_command(
    name="remove_from_playlist",
    description="Remove from playlist; you can only remove a song that you added, unless you are an admin",
    guild_ids=SERVERS,
)
async def remove_from_playlist(ctx: commands.Context, index: Any) -> None:
    try:
        # retrieve the song from playlist at index index
        playlist = await Playlist.retrieve_one(id=index)
        if playlist is None:
            await ctx.respond(f"Could not find the playlist instance with id: {index}")
            return
    except Exception as e:
        await ctx.respond(f"Could not find the playlist instance with id: {index}")
        return
    # check that the song exists in the youtube playlist
    if not await youtube.check_song_in_playlist(playlist.song):
        if not await youtube.sync_playlist(ctx, song=playlist.song):
            await ctx.respond(
                "Could not sync the database with the youtube playlist",
                ephemeral=True,
            )
            return
        # Try again
        playlist = await Playlist.retrieve_one(id=index)
        if playlist is None:
            await ctx.respond(f"Could not find the playlist instance with id: {index}")
            return
        if not await youtube.check_song_in_playlist(playlist.song):
            await ctx.respond(
                "The song you are trying to remove does not exist in the playlist"
            )
            return

    # validate that the user_id matches or that the current user is an admin
    if (
        playlist.user.name != ctx.author.name
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.respond(
            "You can only remove a song that you added, unless you are an admin"
        )
        return
    try:
        # remove the song from the playlist
        await playlist.remove_song(playlist)
        await ctx.respond(
            f"{ctx.author.name} removed {playlist.song.name} from the playlist"
        )
    except Exception as e:
        await ctx.respond(
            f"An error occurred removing the song from the playlist: {str(e)}"
        )
    return
