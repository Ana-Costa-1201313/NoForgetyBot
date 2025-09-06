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
file = 'bdays.json'

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name="hello", description="Replies with hello!")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!!")

@bot.tree.command(name="add_bday", description="Add a birthday! Format: MM-DD")
async def add_bday(interaction: discord.Interaction, name: str, date: str):    
    if not validate_date(date):
        await interaction.response.send_message("Invalid date format. Please use MM-DD.")
        return
    
    bdays = load_birthdays()

    new_bday = {"name": name, "date": date}
    
    bdays["birthdays"].append(new_bday)

    save_birthdays(bdays)

    await interaction.response.send_message(f"{name}'s birthday was added!")

@bot.tree.command(name="check_bdays", description="Check today birthdays!")
async def check_today_birthdays(interaction: discord.Interaction):
    today = datetime.now().strftime("%m-%d")
    bdays = load_birthdays()

    for bday in bdays["birthdays"]:
        if bday["date"] == today:
            await interaction.response.send_message(f"Today is {bday['name']}'s birthday!!")

def validate_date(date: str) -> bool:
    try:
        datetime.strptime(f"2000-{date}", "%Y-%m-%d")
        return True
    except ValueError:
        return False

def load_birthdays():
    with open(file, 'r') as f:
        return json.load(f)

def save_birthdays(bdays):
    with open(file, 'w') as f:
        json.dump(bdays, f, indent=4)

bot.run(TOKEN)