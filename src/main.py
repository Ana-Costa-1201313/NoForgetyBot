import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import birthday
import appointment
from datetime import datetime, time, timedelta

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1412810786492907520

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=None, intents=intents)

birthday.birthday_commands(bot)
appointment.appointment_commands(bot)

@bot.event
async def on_ready():
    await bot.tree.sync()
    if not daily_check.is_running():
        daily_check.start()

@tasks.loop(hours=24)
async def daily_check():
    await discord.utils.sleep_until(datetime.combine(datetime.now().date(), time(9, 30)))

    bdays_messages = birthday.get_today_birthdays()
    appointments_messages = appointment.get_today_appointments()

    channel = bot.get_channel(CHANNEL_ID)

    await channel.send("\n".join(bdays_messages))
    await channel.send("\n".join(appointments_messages))

bot.run(TOKEN)