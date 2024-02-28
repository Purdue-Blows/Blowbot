from utils.constants import SERVERS, bot


@bot.slash_command(
    name="pause",
    description="Pause Blowbot",
    guild_ids=SERVERS,
)
async def pause(ctx, arg):
    return
