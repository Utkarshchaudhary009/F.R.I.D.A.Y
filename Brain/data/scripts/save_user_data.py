import os
import sys
import json

def save_user_data():
    user_details = {
        'Gmail': input("Enter your Gmail: "),
        'phone_number': input("Enter your phone number: "),
        'firstName': input("Enter your First name: "),
        'lastName': input("Enter your Last name: "),
        'school': input("Enter your school: "),
        'hobby': input("Enter your hobby: "),
        'favourite_song': input("Enter your favourite song: "),
        'favourite_movie': input("Enter your favourite movie: ")
    }

    data_folder = "f:\\Friday\\Brain\\data"  # Corrected the path and removed the trailing backslash
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    user_config_path = os.path.join(data_folder, 'userconfig.json')
    with open(user_config_path, 'w') as file:
        json.dump(user_details, file, indent=4)
    
    print("User details saved successfully.")

if __name__ == "__main__":
    save_user_data()
