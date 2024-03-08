from utils.constants import MAX_MESSAGE_LENGTH
from discord.ext import commands


async def send_message_in_parts(
    ctx: commands.Context, message: str, ephemeral: bool = True
) -> None:
    if len(message) > MAX_MESSAGE_LENGTH:
        while len(message) > MAX_MESSAGE_LENGTH:
            await ctx.send(message[:MAX_MESSAGE_LENGTH], ephemeral=ephemeral)
            message = message[MAX_MESSAGE_LENGTH:]
    else:
        await ctx.send(message, ephemeral=ephemeral)
    return
