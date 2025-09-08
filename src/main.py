import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import birthday
import appointment

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)

birthday.birthday_commands(bot)
appointment.appointment_commands(bot)

@bot.event
async def on_ready():
    await bot.tree.sync()

bot.run(TOKEN)