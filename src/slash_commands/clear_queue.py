import traceback
from typing import Any

from discord.ext import commands

from utils.constants import SERVERS, Session, bot
from services import discord_service
from utils.messages import ADMIN_ONLY_ERROR, GENERIC_ERROR, NO_GUILD_ERROR

from models.queue import Queue

QUEUE_CLEARED_MESSAGE = "Queue was cleared by {author}"


# Clears the bots queue
# Can only be run if the caller is an admin in the server
@bot.slash_command(
    name="clear_queue",
    description="Clear the current queue (if you are an admin)",
    guild_ids=SERVERS,
)
async def clear_queue(ctx) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        try:
            # check if admin
            if discord_service.is_admin(ctx.author):  # type: ignore
                # clear the queue
                await Queue.clear_queue(session, ctx.guild.id)
                # return a success message as confirmation
                await ctx.send(QUEUE_CLEARED_MESSAGE.format(author=ctx.author.name))
            # can't clear queue if not an admin
            else:
                await ctx.respond(
                    ADMIN_ONLY_ERROR.format("clear_queue"), ephemeral=True
                )
        except Exception:
            await ctx.respond(GENERIC_ERROR.format("clear_queue"), ephemeral=True)
            traceback.print_exc()
        return
