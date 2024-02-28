import discord
from discord.ext import commands

intents = discord.Intents.default() | discord.Intents.members

# Initialize bot
bot = commands.Bot(intents=intents)
