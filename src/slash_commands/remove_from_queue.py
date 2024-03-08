from discord.ext import commands
from utils.constants import DB_CLIENT, SERVERS, bot
from models.queue import Queue


RESPONSE_QUEUE_NOT_FOUND = "Could not find the queue instance with id: {index}"
RESPONSE_CANNOT_REMOVE_SONG = (
    "You can only remove a song that you added, unless you are an admin"
)
RESPONSE_SONG_REMOVED = "{ctx.author.name} removed {queue.song.name} from the queue"
RESPONSE_ERROR_REMOVING_SONG = "An error occurred removing the song from the queue"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.command(
    name="remove_from_queue",
    description="Remove the song at the index specified that you added to the queue (or any song if you are an admin)",
    guild_ids=SERVERS,
)
async def remove_from_queue(ctx: commands.Context, index: int):
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    try:
        # retrieve the song from playlist at index index
        queue = await Queue.retrieve_one(db, id=index)
        if queue is None:
            await ctx.send(RESPONSE_QUEUE_NOT_FOUND.format(index=index))
            return
    except Exception as e:
        await ctx.send(RESPONSE_QUEUE_NOT_FOUND.format(index=index))
        return

    # validate that the user_id matches or that the current user is an admin
    if (
        queue.user.name != ctx.author.name
        and not ctx.author.guild_permissions.administrator  # type: ignore
    ):
        await ctx.send(RESPONSE_CANNOT_REMOVE_SONG)
        return
    try:
        # remove the song from the playlist
        await queue.remove_song(db, queue)
        await ctx.send(RESPONSE_SONG_REMOVED.format(ctx=ctx, queue=queue))
    except Exception as e:
        await ctx.send(RESPONSE_ERROR_REMOVING_SONG)
    return
