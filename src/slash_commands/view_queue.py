from discord.ext import commands
from utils.constants import SERVERS, Session, bot
from models.songs import Song
from models.queue import Queue
from utils.send_message_in_parts import send_message_in_parts
from utils.messages import COULD_NOT_FIND_ERROR, NO_GUILD_ERROR


# View the current queue
# Displays num_to_display songs
QUEUE_EMPTY_MESSAGE = "The queue is empty"


@bot.slash_command(
    name="view_queue", description="View the current queue", guild_ids=SERVERS
)
async def view_queue(ctx, num_to_display: int = 3) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # create a message that formats the first num_to_display songs in queue
        message = ""
        for i in range(num_to_display):
            next_queue_num = await Queue.get_next_queue_num(session, ctx.guild.id)
            if next_queue_num is None:
                await ctx.respond(COULD_NOT_FIND_ERROR.format("queue"), ephemeral=True)
                return
            queue = await Queue.retrieve_one(
                session, ctx.guild.id, id=next_queue_num + i
            )
            if queue is None:
                await ctx.respond(COULD_NOT_FIND_ERROR.format("queue"), ephemeral=True)
                return
            formatted_song = Song.format_song(queue.song)
            if formatted_song is not None:
                message += formatted_song + "\n"
        if message == "":
            await ctx.respond(QUEUE_EMPTY_MESSAGE, ephemeral=True)
            return
        # check that the message isn't too long; if it is, split it up into multiple messages
        await send_message_in_parts(ctx, message)
        return
