import os
import sys

# Add parent directory to sys.path to make relative imports work
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if parent_dir not in sys.path:
    print(f"{parent_dir}\scripts")
    sys.path.append(f"{parent_dir}\scripts")

import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_credentials():
    gmail = input("Enter your Gmail: ")
    password = input("Enter your password: ")

    hashed_password = hash_password(password)
    
    credentials = {
        'Gmail': gmail,
        'Password': hashed_password
    }

    data_folder = "f:\\Friday\\Brain\\data"  
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    credentials_path = os.path.join(data_folder, 'credentials.crc')
    with open(credentials_path, 'w') as file:
        for key, value in credentials.items():
            file.write(f"{key}: {value}\n")

    print("Credentials saved securely.")
