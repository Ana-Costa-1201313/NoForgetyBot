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
bdays_file = 'bdays.json'
appointments_file = 'appointments.json'

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name="add_bday", description="Add a birthday! Format: MM-DD")
async def add_bday(interaction: discord.Interaction, name: str, date: str):    
    if not validate_date(date):
        await interaction.response.send_message("Invalid date format. Please use MM-DD.")
        return
    
    bdays = load_data(bdays_file)

    new_bday = {"name": name, "date": date}
    
    bdays["birthdays"].append(new_bday)

    save_data(bdays_file, bdays)

    await interaction.response.send_message(f"{name}'s birthday was added!")

@bot.tree.command(name="check_bdays", description="Check today birthdays!")
async def check_today_birthdays(interaction: discord.Interaction):
    today = datetime.now().strftime("%m-%d")
    bdays = load_data(bdays_file)

    messages = []
    
    for bday in bdays["birthdays"]:
        if bday["date"] == today:
            messages.append(f"Don't forget: Today is {bday['name']}'s birthday!! 🎉🎂")
    
    if not messages:
        messages.append("No birthdays today!")

    await interaction.response.send_message("\n".join(messages))

@bot.tree.command(name="add_appointment", description="Add an appointment! Format: MM-DD")
async def add_appointment(interaction: discord.Interaction, name: str, date: str):    
    if not validate_date(date):
        await interaction.response.send_message("Invalid date format. Please use MM-DD.")
        return

    appointments = load_data(appointments_file)

    new_appointment = {"name": name, "date": date}

    appointments["appointments"].append(new_appointment)

    save_data(appointments_file, appointments)

    await interaction.response.send_message(f"Appointment: {name} was added!")

@bot.tree.command(name="check_appointments", description="Check today appointments!")
async def check_today_appointments(interaction: discord.Interaction):
    today = datetime.now().strftime("%m-%d")
    appointments = load_data(appointments_file)

    messages = []
    
    for appointment in appointments["appointments"]:
        if appointment["date"] == today:
            messages.append(f"Don't forget: {appointment['name']}!! ⏰")
    
    if not messages:
        messages.append("No appointments today!")

    await interaction.response.send_message("\n".join(messages))

def validate_date(date: str) -> bool:
    try:
        datetime.strptime(f"2000-{date}", "%Y-%m-%d")
        return True
    except ValueError:
        return False

def load_data(file: str):
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

bot.run(TOKEN)