from models.queue import Queue
from discord_service import pause, play_song
from utils.constants import DB_CLIENT, SERVERS, bot, db
from utils.state import QUEUE_NUM, CURRENT_SONG
from discord.ext import commands


# Define constants for response messages
NO_NEXT_SONG_MESSAGE = (
    "Could not skip to the next song because there IS no next song in the queue"
)
PLAYING_PREVIOUS_SONG_MESSAGE = (
    "Playing the previous song again at {ctx.author.name}'s request"
)
SKIP_ERROR_MESSAGE = "Sorry, an error occurred while trying to skip the song"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.command(
    name="skip",
    description="Skip the current song",
    guild_ids=SERVERS,
)
async def skip(ctx: commands.Context):
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    global QUEUE_NUM
    global CURRENT_SONG
    # update queue_num and current_song accordingly and the db
    QUEUE_NUM += 1
    try:
        queue_count = await db.queue.count_documents({})
        if QUEUE_NUM > queue_count:
            QUEUE_NUM -= 1
            await ctx.send(NO_NEXT_SONG_MESSAGE)
            return

        # Pause the current song
        await pause()

        # Retrieve the next song from the queue
        CURRENT_SONG = Queue.retrieve_one(QUEUE_NUM)

        # play the previous song again
        await play_song()

        # return a success message as confirmation
        await ctx.send(PLAYING_PREVIOUS_SONG_MESSAGE)
        return
    except Exception as e:
        await ctx.send(SKIP_ERROR_MESSAGE.format(str(e)))
