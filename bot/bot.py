import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.members = True  # needed for some discord.py features

bot = commands.Bot(command_prefix="!", intents=intents)  # replace "!" with your preferred command prefix

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')

for filename in os.listdir('./bot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'bot.cogs.{filename[:-3]}')

bot.run(TOKEN)
