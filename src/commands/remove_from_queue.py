from typing import Union
from discord.ext import commands
from utils.constants import SERVERS, bot, cur
from models.songs import Song
from models.queue import Queue
from services import youtube


@bot.slash_command(
    name="remove_from_queue",
    description="Remove the song at the index specified that you added to the queue (or any song if you are an admin)",
    guild_ids=SERVERS,
)
async def remove_from_queue(ctx: commands.Context, index: Union[int, str]):
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
    queue = Queue.from_map(result)
    # validate that the user_id matches or that the current user is an admin
    if (
        queue.user.name != ctx.author.name
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.respond(
            "You can only remove a song that you added, unless you are an admin"
        )
        return
    # remove the song from the playlist
    cur.execute("DELETE FROM queue WHERE id = ?", (index,))
    # return a success message as confirmation
    await ctx.respond(f"{ctx.author.name} removed {song.name} from the queue")
    return
