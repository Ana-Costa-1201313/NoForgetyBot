import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot connected!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands!')
    except Exception as e:
        print(e)

@bot.tree.command(name="test", description="Replies with hello")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!!")

bot.run(TOKEN)