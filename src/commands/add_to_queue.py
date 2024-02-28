from utils.constants import SERVERS, bot


@bot.slash_command(
    name="add_to_queue", description="Add a song to Blowbot's queue", guild_ids=SERVERS
)
async def add_to_queue(ctx, arg):
    return
