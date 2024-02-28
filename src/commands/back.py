from utils.constants import SERVERS, bot


@bot.slash_command(
    name="back",
    description="Relisten to the previous song (if it exists)",
    guild_ids=SERVERS,
)
async def back(ctx, arg):
    return
