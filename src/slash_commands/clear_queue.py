from typing import Any

from discord.ext import commands

from utils.constants import SERVERS, bot
from services import discord
from models.queue import Queue


QUEUE_CLEARED_MESSAGE = "Queue was cleared by {author}"
ADMIN_ONLY_MESSAGE = "Only admins can clear the queue"


# Clears the bots queue
# Can only be run if the caller is an admin in the server
@bot.slash_command(
    name="clear_queue",
    description="Clear the current queue (if you are an admin)",
    guild_ids=SERVERS,
)
async def clear_queue(ctx: commands.Context) -> None:
    # check if admin
    if discord.is_admin(ctx.author):
        # clear the queue
        await Queue.clear_queue()
        # return a success message as confirmation
        await ctx.respond(QUEUE_CLEARED_MESSAGE.format(author=ctx.author.name))
    # can't clear queue if not an admin
    else:
        await ctx.respond(ADMIN_ONLY_MESSAGE, ephemeral=True)
    return
