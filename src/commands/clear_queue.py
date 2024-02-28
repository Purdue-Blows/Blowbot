from utils.constants import SERVERS, bot


@bot.slash_command(
    name="clear_queue",
    description="Clear the current queue (if you are an admin)",
    guild_ids=SERVERS,
)
async def clear_queue(ctx, arg):
    return
