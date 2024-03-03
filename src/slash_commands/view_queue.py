from math import e
from typing import Optional
from discord.ext import commands
from utils.constants import MAX_MESSAGE_LENGTH, SERVERS, bot
from models.songs import Song
from models.queue import Queue
from utils.functions import send_message_in_parts


# View the current queue
# Displays num_to_display songs
@bot.slash_command(
    name="view_queue", description="View the current queue", guild_ids=SERVERS
)
async def view_queue(ctx: commands.Context, num_to_display: int = 3) -> None:
    # create a message that formats the first num_to_display songs in queue
    message = ""
    for i in range(num_to_display):
        queue = await Queue.retrieve_one(i)
        if queue is None:
            break
        formatted_song = await Song.format_song(queue.song)
        if formatted_song is not None:
            message += formatted_song + "\n"
    if message == "":
        await ctx.respond("The queue is empty", ephemeral=True)
        return
    # check that the message isn't too long; if it is, split it up into multiple messages
    await send_message_in_parts(ctx, message)
    return
