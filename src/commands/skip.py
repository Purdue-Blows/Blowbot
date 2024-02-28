from utils.constants import SERVERS, bot


@bot.slash_command(
    name="skip",
    description="Skip the current song",
    guild_ids=SERVERS,
)
async def skip(ctx, arg):
    return
