import discord
from datetime import datetime
from utils import validate_date, load_data, save_data

APPOINTMENTS_FILE = 'appointments.json'

def get_today_appointments():
    today = datetime.now().strftime("%m-%d")
    appointments = load_data(APPOINTMENTS_FILE)

    messages = []
    
    for appointment in appointments["appointments"]:
        if appointment["date"] == today:
            messages.append(f"Don't forget: {appointment['name']}!! ⏰")
    
    if not messages:
        messages.append("No appointments today!")

    return messages

def appointment_commands(bot):
    @bot.tree.command(name="add_appointment", description="Add an appointment! Format: MM-DD")
    async def add_appointment(interaction: discord.Interaction, name: str, date: str):    
        if not validate_date(date):
            await interaction.response.send_message("Invalid date format. Please use MM-DD.")
            return

        appointments = load_data(APPOINTMENTS_FILE)

        new_appointment = {"name": name, "date": date}

        appointments["appointments"].append(new_appointment)

        save_data(APPOINTMENTS_FILE, appointments)

        await interaction.response.send_message(f"Appointment: {name} was added!")

    @bot.tree.command(name="check_today_appointments", description="Check today appointments!")
    async def check_today_appointments(interaction: discord.Interaction):
        messages = get_today_appointments()

        await interaction.response.send_message("\n".join(messages))

    @bot.tree.command(name="list_all_appointments", description="List all appointments!")
    async def list_appointments(interaction: discord.Interaction):
        appointments = load_data(APPOINTMENTS_FILE)

        appointment_list = []

        for appointment in appointments["appointments"]:
            appointment_list.append(f"{appointment['name']}: {appointment['date']}")

        if not appointment_list:
            appointment_list.append("No appointments found!")

        await interaction.response.send_message("\n".join(appointment_list))

    @bot.tree.command(name="remove_appointment", description="Remove a appointment! Format: MM-DD")
    async def remove_appointment(interaction: discord.Interaction, name: str, date: str):
        if not validate_date(date):
            await interaction.response.send_message("Invalid date format. Please use MM-DD.")

        removed = False

        appointments = load_data(APPOINTMENTS_FILE)

        for appointment in appointments["appointments"]:
            if appointment["name"] == name and appointment["date"] == date:
                appointments["appointments"].remove(appointment)
                removed = True

        if not removed:
            await interaction.response.send_message(f"No appointment found for {name} at {date}.")
            return

        save_data(APPOINTMENTS_FILE, appointments)

        await interaction.response.send_message(f"Appointment: {name} at {date} was removed!")
