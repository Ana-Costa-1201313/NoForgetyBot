import discord
from datetime import datetime
from utils import validate_date, load_data, save_data

BDAYS_FILE = 'bdays.json'

def get_today_birthdays():
    today = datetime.now().strftime("%m-%d")
    bdays = load_data(BDAYS_FILE)

    messages = []
        
    for bday in bdays["birthdays"]:
        if bday["date"] == today:
            messages.append(f"Don't forget: Today is {bday['name']}'s birthday!! 🎉🎂")
    
    if not messages:
        messages.append("No birthdays today!")

    return messages

def birthday_commands(bot):
    @bot.tree.command(name="add_bday", description="Add a birthday! Format: MM-DD")
    async def add_bday(interaction: discord.Interaction, name: str, date: str):    
        if not validate_date(date):
            await interaction.response.send_message("Invalid date format. Please use MM-DD.")
            return
        
        bdays = load_data(BDAYS_FILE)

        new_bday = {"name": name, "date": date}
        
        bdays["birthdays"].append(new_bday)

        save_data(BDAYS_FILE, bdays)

        await interaction.response.send_message(f"{name}'s birthday was added!")

    @bot.tree.command(name="check_today_bdays", description="Check today birthdays!")
    async def check_today_birthdays(interaction: discord.Interaction):
        messages = get_today_birthdays()

        await interaction.response.send_message("\n".join(messages))

    @bot.tree.command(name="list_all_bdays", description="List all birthdays!")
    async def list_birthdays(interaction: discord.Interaction):
        bdays = load_data(BDAYS_FILE)

        bday_list = []

        for bday in bdays["birthdays"]:
            bday_list.append(f"{bday['name']}: {bday['date']}")

        if not bday_list:
            bday_list.append("No birthdays found!")

        await interaction.response.send_message("\n".join(bday_list))

    @bot.tree.command(name="remove_bday", description="Remove a birthday! Format: MM-DD")
    async def remove_birthday(interaction: discord.Interaction, name: str, date: str):
        if not validate_date(date):
            await interaction.response.send_message("Invalid date format. Please use MM-DD.")

        removed = False

        bdays = load_data(BDAYS_FILE)

        for bday in bdays["birthdays"]:
            if bday["name"] == name and bday["date"] == date:
                bdays["birthdays"].remove(bday)
                removed = True

        if not removed:
            await interaction.response.send_message(f"No birthday found for {name} at {date}.")
            return

        save_data(BDAYS_FILE, bdays)

        await interaction.response.send_message(f"{name}'s birthday at {date} was removed!")
