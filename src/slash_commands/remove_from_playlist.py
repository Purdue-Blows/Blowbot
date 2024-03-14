from math import e
import traceback
from models.playlist import Playlist
from models.songs import Song
from models.playback import Playback
from utils.constants import SERVERS, Session, bot, ydl
from services import youtube_service
from discord.ext import commands
from typing import Any
from utils.messages import ADMIN_ONLY_ERROR, NO_GUILD_ERROR


RESPONSE_NOT_FOUND = "Could not find the playlist instance with id: {index}"
RESPONSE_SYNC_ERROR = "Could not sync the database with the youtube playlist"
RESPONSE_SONG_NOT_FOUND = (
    "The song you are trying to remove does not exist in the playlist"
)
RESPONSE_REMOVED = "{ctx.author.name} removed {playlist.song.name} from the playlist"
SONG_REMOVED_ERROR = "Sorry, an error occurred removing the song from the playlist"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.slash_command(
    name="remove_from_playlist",
    description="Remove from playlist; you can only remove a song that you added, unless you are an admin",
    guild_ids=SERVERS,
)
async def remove_from_playlist(ctx, index: int) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        try:
            # retrieve the song from playlist at index index
            playlist = await Playlist.retrieve_one(session, ctx.guild.id, id=index)
            if playlist is None:
                await ctx.respond(
                    RESPONSE_NOT_FOUND.format(index=index), ephemeral=True
                )
                return
        except Exception as e:
            await ctx.respond(RESPONSE_NOT_FOUND.format(index=index), ephemeral=True)
            traceback.print_exc()
            return
        # check that the song exists in the youtube playlist
        if not await youtube_service.check_song_in_playlist(ydl, playlist.song):
            current_playlist = await Playback.get_current_playlist(
                session, ctx.guild.id
            )
            if not await youtube_service.sync_playlist(
                session, ctx.guild.id, ydl, current_playlist
            ):
                await ctx.respond(RESPONSE_SYNC_ERROR, ephemeral=True)
                return
            # Try again
            playlist = await Playlist.retrieve_one(session, ctx.guild.id, id=index)
            if playlist is None:
                await ctx.respond(
                    RESPONSE_NOT_FOUND.format(index=index), ephemeral=True
                )
                return
            if not await youtube_service.check_song_in_playlist(ydl, playlist.song):
                await ctx.respond(RESPONSE_SONG_NOT_FOUND, ephemeral=True)
                return

        # validate that the user_id matches or that the current user is an admin
        # Anyone can remove a song associated with a None user though
        if playlist.user != None:
            if (
                playlist.user.name != ctx.author.name
                and not ctx.author.guild_permissions.administrator  # type: ignore
            ):
                await ctx.respond(
                    ADMIN_ONLY_ERROR.format("remove_from_playlist"), ephemeral=True
                )
                return
        try:
            # remove the song from the playlist
            await playlist.remove_song(session, playlist)
            await ctx.send(RESPONSE_REMOVED.format(ctx=ctx, playlist=playlist))
        except Exception as e:
            await ctx.respond(SONG_REMOVED_ERROR, ephemeral=True)
            traceback.print_exc()
        return
