from utils.constants import SERVERS, bot
from utils.state import QUEUE_NUM, CURRENT_SONG
from models.queue import Queue
from services.discord import play_song
from discord.ext import commands


@bot.slash_command(
    name="back",
    description="Relisten to the previous song (if it exists)",
    guild_ids=SERVERS,
)
async def back(ctx: commands.Context) -> None:
    global QUEUE_NUM
    global CURRENT_SONG
    # update queue_num and current_song accordingly and the db
    QUEUE_NUM -= 1
    if QUEUE_NUM < 0:
        QUEUE_NUM = 0
        await ctx.respond(
            f"Could not go back to the previous song because there IS no previos song in the queue"
        )
        return
    CURRENT_SONG = Queue.retrieve_one(QUEUE_NUM)

    # play the previous song again
    await play_song()

    # return a success message as confirmation
    await ctx.respond(f"Playing the previous song again at {ctx.author.name}'s request")
