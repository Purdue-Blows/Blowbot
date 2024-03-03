from discord.ext import commands
from utils.constants import MAX_MESSAGE_LENGTH


async def send_message_in_parts(ctx: commands.Context, message: str) -> None:
    if len(message) > MAX_MESSAGE_LENGTH:
        while len(message) > MAX_MESSAGE_LENGTH:
            await ctx.respond(message[:MAX_MESSAGE_LENGTH])
            message = message[MAX_MESSAGE_LENGTH:]
    else:
        await ctx.respond(message)
    return
