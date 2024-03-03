from typing import Union
from discord.ext import commands
from utils.constants import SERVERS, bot, con
from models.songs import Song
from models.queue import Queue
from services import youtube


@bot.slash_command(
    name="remove_from_queue",
    description="Remove the song at the index specified that you added to the queue (or any song if you are an admin)",
    guild_ids=SERVERS,
)
async def remove_from_queue(ctx: commands.Context, index: int):
    try:
        # retrieve the song from playlist at index index
        queue = await Queue.retrieve_one(id=index)
        if queue is None:
            await ctx.respond(f"Could not find the queue instance with id: {index}")
            return
    except Exception as e:
        await ctx.respond(f"Could not find the queue instance with id: {index}")
        return

    # validate that the user_id matches or that the current user is an admin
    if (
        queue.user.name != ctx.author.name
        and not ctx.author.guild_permissions.administrator
    ):
        await ctx.respond(
            "You can only remove a song that you added, unless you are an admin"
        )
        return
    try:
        # remove the song from the playlist
        await queue.remove_song(queue)
        await ctx.respond(f"{ctx.author.name} removed {queue.song.name} from the queue")
    except Exception as e:
        await ctx.respond(
            f"An error occurred removing the song from the queue: {str(e)}"
        )
    return
