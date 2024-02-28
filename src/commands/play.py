from utils.constants import SERVERS, bot


@bot.slash_command(
    name="play",
    description="Attempt to resume blowbot playback",
    guild_ids=SERVERS,
)
async def play(ctx, arg):
    return
