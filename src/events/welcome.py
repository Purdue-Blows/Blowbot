from bot import bot
from utils.constants import (
    SERVERS,
    PURDUE_BLOWS_CHANNEL_IDS,
    BOT_DEBUGGING_SERVER_CHANNEL_IDS,
)


# Event handler for member join
@bot.event
async def on_member_join(member):
    # Welcome message channel
    general_channel = member.guild.system_channel

    # Welcome message content
    welcome_message = f"Welcome to the server, {member.name}! :wave:"

    # Send the welcome message
    await general_channel.send(welcome_message)
