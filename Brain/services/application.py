import os
import json
import os
import sys
# Ensure the parent directory is in sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file_path = os.path.join(base_dir, 'data', 'application_map.json')

def open_application(arguments):
    application = arguments.get("application").lower().replace("ms","").replace("microsoft","")

    if not application:
        return {"response": "Please specify the application to open."}

    try:
        # Load application map from JSON file
        with open(data_file_path, 'r') as file:
            app_map = json.load(file)

        # Find the command to run the application
        app_command = app_map.get(application.strip())

        if app_command:
            os.system(app_command)
            return {"response": f"Opening {application}."}
        else:
            try:
                os.system(f"start {application.lower()}")
            except:
                return {"response": f"I don't know how to open {application}."}

    except Exception as e:
        return {"response": f"An error occurred while opening the application: {str(e)}"}
