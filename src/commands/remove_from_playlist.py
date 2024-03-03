from models.playlist import Playlist
from models.songs import Song
from utils.constants import SERVERS, bot, cur
from services import youtube
from discord.ext import commands
from typing import Any


@bot.slash_command(
    name="remove_from_playlist",
    description="Remove from playlist; you can only remove a song that you added, unless you are an admin",
    guild_ids=SERVERS,
)
async def remove_from_playlist(ctx: commands.Context, index: Any) -> None:
    # retrieve the song from playlist at index index
    result = cur.execute("SELECT * FROM playlist WHERE id = ?", (index,))
    result = result.fetchone()
    song = Song.from_map(result[1])
    # check that the song exists in the youtube playlist
    if not await youtube.check_song_in_playlist(song):
        await youtube.sync_playlist()
        # Try again
        result = cur.execute("SELECT * FROM playlist WHERE id = ?", (index,))
        result = result.fetchone()
        song = Song.from_map(result[1])
        if not await youtube.check_song_in_playlist(song):
            await ctx.respond(
                "The song you are trying to remove does not exist in the playlist"
            )
            return
    playlist = Playlist.from_map(result)
    # validate that the user_id matches or that the current user is an admin
    if (
        playlist.user.name != ctx.author.name
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.respond(
            "You can only remove a song that you added, unless you are an admin"
        )
        return
    # remove the song from the playlist
    cur.execute("DELETE FROM playlist WHERE id = ?", (index,))
    # return a success message as confirmation
    await ctx.respond(f"{ctx.author.name} removed {song.name} from the playlist")
    return
