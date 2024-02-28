from utils.constants import SERVERS, bot


@bot.slash_command(
    name="jazzle",
    description="Determine the jazz standard based on a number of hints. How many tries can you get it in?",
    guild_ids=SERVERS,
)
async def jazzle(ctx, arg):
    await ctx.respond(
        "Sorry, this command hasn't been implemented yet!", ephemeral=True
    )
