import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json
from pathlib import Path

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

@bot.tree.command(name="test", description="Replies with hello!")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!!")

@bot.tree.command(name="add_bday", description="Add a birthday!")
async def add_bday(interaction: discord.Interaction, name: str, date: str):
    bdays = load_birthdays()

    new_bday = {"name": name, "date": date}
    
    bdays["birthdays"].append(new_bday)

    save_birthdays(bdays)

    await interaction.response.send_message(f"{name}'s birthday was added!")

def load_birthdays():
    with open('bdays.json', 'r') as f:
        return json.load(f)

def save_birthdays(bdays):
    with open('bdays.json', 'w') as f:
        json.dump(bdays, f, indent=4)

bot.run(TOKEN)