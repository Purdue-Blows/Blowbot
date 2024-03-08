from math import e
from models.playlist import Playlist
from models.songs import Song
from utils.constants import DB_CLIENT, SERVERS, bot
from services import youtube_service
from discord.ext import commands
from typing import Any


RESPONSE_NOT_FOUND = "Could not find the playlist instance with id: {index}"
RESPONSE_SYNC_ERROR = "Could not sync the database with the youtube playlist"
RESPONSE_SONG_NOT_FOUND = (
    "The song you are trying to remove does not exist in the playlist"
)
RESPONSE_PERMISSION_ERROR = (
    "You can only remove a song that you added, unless you are an admin"
)
RESPONSE_REMOVED = "{ctx.author.name} removed {playlist.song.name} from the playlist"
SONG_REMOVED_ERROR = "Sorry, an error occurred removing the song from the playlist"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.command(
    name="remove_from_playlist",
    description="Remove from playlist; you can only remove a song that you added, unless you are an admin",
    guild_ids=SERVERS,
)
async def remove_from_playlist(ctx: commands.Context, index: int) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    try:
        # retrieve the song from playlist at index index
        playlist = await Playlist.retrieve_one(id=index)
        if playlist is None:
            await ctx.send(RESPONSE_NOT_FOUND.format(index=index))
            return
    except Exception as e:
        await ctx.send(RESPONSE_NOT_FOUND.format(index=index))
        return
    # check that the song exists in the youtube playlist
    if not await youtube_service.check_song_in_playlist(playlist.song):
        if not await youtube_service.sync_playlist():
            await ctx.send(RESPONSE_SYNC_ERROR, ephemeral=True)
            return
        # Try again
        playlist = await Playlist.retrieve_one(id=index)
        if playlist is None:
            await ctx.send(RESPONSE_NOT_FOUND.format(index=index))
            return
        if not await youtube_service.check_song_in_playlist(playlist.song):
            await ctx.send(RESPONSE_SONG_NOT_FOUND)
            return

    # validate that the user_id matches or that the current user is an admin
    # Anyone can remove a song associated with a None user though
    if playlist.user != None:
        if (
            playlist.user.name != ctx.author.name
            and not ctx.author.guild_permissions.administrator  # type: ignore
        ):
            await ctx.send(RESPONSE_PERMISSION_ERROR)
            return
    try:
        # remove the song from the playlist
        await playlist.remove_song(playlist)
        await ctx.send(RESPONSE_REMOVED.format(ctx=ctx, playlist=playlist))
    except Exception as e:
        await ctx.send(SONG_REMOVED_ERROR)
    return
