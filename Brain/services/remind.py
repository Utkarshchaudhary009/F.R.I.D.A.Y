import json
from datetime import datetime

def set_reminder_and_write_to_file(arguments):
    reminder_time = arguments.get('time')
    reminder_message = arguments.get('message')

    if reminder_time and reminder_message:
        reminder_data = {
            "reminder_time": reminder_time,
            "reminder_message": reminder_message
        }

        with open('../data/reminder.json', 'w') as file:
            json.dump(reminder_data, file)

        return {"response": f"Reminder set for {reminder_time}: {reminder_message}"}

    return {"response": "Failed to set reminder. Please provide a valid time and message."}

def start_remind():
    try:
        with open('../data/reminder.json', 'r+') as file:
            reminder_data = json.load(file)

            reminder_time = reminder_data.get('reminder_time')
            reminder_message = reminder_data.get('reminder_message')

            if reminder_time and reminder_message:
                reminder_datetime = datetime.strptime(reminder_time, '%Y-%m-%d %H:%M:%S')
                if reminder_datetime <= datetime.now():
                    print(f"Reminder: {reminder_message}")
                    # Clear the reminder after showing it
                    file.seek(0)
                    file.truncate()
                    json.dump({}, file)

    except FileNotFoundError:
        print("No reminder found!")
    except json.JSONDecodeError:
        print("Reminder file is empty or corrupt!")
