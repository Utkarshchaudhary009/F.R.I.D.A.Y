import os
import json

def open_application(arguments):
    application = arguments.get("application")

    if not application:
        return {"response": "Please specify the application to open."}

    try:
        # Load application map from JSON file
        with open('Brain/application_map.json', 'r') as file:
            app_map = json.load(file)

        # Find the command to run the application
        app_command = app_map.get(application.lower())

        if app_command:
            os.system(app_command)
            return {"response": f"Opening {application}."}
        else:
            return {"response": f"I don't know how to open {application}."}

    except Exception as e:
        return {"response": f"An error occurred while opening the application: {str(e)}"}
