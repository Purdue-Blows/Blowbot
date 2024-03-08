from models.songs import Song
from utils.constants import DB_CLIENT, SERVERS, bot
from models.queue import Queue
from discord_service import play_song
from discord.ext import commands


BACK_NO_PREVIOUS_SONG_MESSAGE = "Could not go back to the previous song because there IS no previous song in the queue"
BACK_SUCCESS_MESSAGE = "Playing the previous song again at {ctx.author.name}'s request"
COULD_NOT_FIND_SONG = "There was an error finding the previous song"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.command(
    name="back",
    description="Relisten to the previous song (if it exists)",
    guild_ids=SERVERS,
)
async def back(ctx: commands.Context) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # update queue_num and current_song accordingly and the db
    queue_num -= 1
    if queue_num < 0:
        queue_num = 0
        await ctx.send(BACK_NO_PREVIOUS_SONG_MESSAGE)
        return
    queue = await Queue.retrieve_one(db, current_song.id)

    # play the previous song again
    if queue != None:
        await play_song(queue.audio)
    else:
        await ctx.send(BACK_NO_PREVIOUS_SONG_MESSAGE)
        return

    # return a success message as confirmation
    await ctx.send(BACK_SUCCESS_MESSAGE)
