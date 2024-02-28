from utils.constants import SERVERS, bot


@bot.slash_command(
    name="profile",
    description="Get information about your current user profile",
    guild_ids=SERVERS,
)
async def profile(ctx):
    await ctx.respond(
        "Sorry, this command hasn't been implemented yet!", ephemeral=True
    )
