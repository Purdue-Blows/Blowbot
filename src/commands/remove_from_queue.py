from utils.constants import SERVERS
from bot import bot


@bot.slash_command(
    name="remove_from_queue",
    description="Remove a song that you added to the queue (or a song in general if you are an admin)",
    guild_ids=SERVERS,
)
async def remove_from_queue(ctx, arg):
    return
