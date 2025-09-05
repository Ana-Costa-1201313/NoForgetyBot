import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import json
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()

bot = commands.Bot(command_prefix=None, intents=intents)

@bot.event
async def on_ready():
    print('Bot connected!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands!')
    except Exception as e:
        print(e)

@bot.tree.command(name="hello", description="Replies with hello!")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!!")

@bot.tree.command(name="add_bday", description="Add a birthday! Format: MM-DD")
async def add_bday(interaction: discord.Interaction, name: str, date: str):
    try:
        datetime.strptime(f"2000-{date}", "%Y-%m-%d")
    except ValueError:
        await interaction.response.send_message("Invalid date format. Please use MM-DD.")
        return   
    
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