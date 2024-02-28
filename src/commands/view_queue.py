from utils.constants import SERVERS, bot


@bot.slash_command(
    name="view_queue", description="View the current queue", guild_ids=SERVERS
)
async def view_queue(ctx, arg):
    return
