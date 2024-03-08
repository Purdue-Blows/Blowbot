from typing import Any

from discord.ext import commands

from utils.constants import DB_CLIENT, SERVERS, bot
from services import discord_service
from models.queue import Queue

QUEUE_CLEARED_MESSAGE = "Queue was cleared by {author}"
ADMIN_ONLY_MESSAGE = "Only admins can clear the queue"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


# Clears the bots queue
# Can only be run if the caller is an admin in the server
@bot.command(
    name="clear_queue",
    description="Clear the current queue (if you are an admin)",
    guild_ids=SERVERS,
)
async def clear_queue(ctx: commands.Context) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # check if admin
    if discord_service.is_admin(ctx.author):  # type: ignore
        # clear the queue
        await Queue.clear_queue(db)
        # return a success message as confirmation
        await ctx.send(QUEUE_CLEARED_MESSAGE.format(author=ctx.author.name))
    # can't clear queue if not an admin
    else:
        await ctx.send(ADMIN_ONLY_MESSAGE, ephemeral=True)
    return
