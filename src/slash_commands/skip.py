from models.queue import Queue
from services.discord import pause, play_song
from utils.constants import SERVERS, bot, con
from utils.state import QUEUE_NUM, CURRENT_SONG
from discord.ext import commands
from typing import Optional


@bot.slash_command(
    name="skip",
    description="Skip the current song",
    guild_ids=SERVERS,
)
async def skip(ctx: commands.Context):
    global QUEUE_NUM
    global CURRENT_SONG
    # update queue_num and current_song accordingly and the db
    QUEUE_NUM += 1
    try:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM queue")
        queue_count = cur.fetchone()[0]
        if QUEUE_NUM > queue_count:
            QUEUE_NUM -= 1
            await ctx.respond(
                f"Could not skip to the next song because there IS no next song in the queue"
            )
            return

        # Pause the current song
        await pause()

        # Retrieve the next song from the queue
        CURRENT_SONG = Queue.retrieve_one(QUEUE_NUM)

        # play the previous song again
        await play_song()

        # return a success message as confirmation
        await ctx.respond(
            f"Playing the previous song again at {ctx.author.name}'s request"
        )
        return
    except Exception as e:
        await ctx.respond(f"An error occurred: {str(e)}")
    finally:
        if cur:
            cur.close()
