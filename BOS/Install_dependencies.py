import subprocess
import os

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {command}\n{e}")

def setup_cricket_api():
    os.chdir("Brain/services/")
    # Step 1: Clone the Repository
    run_command("git clone https://github.com/sanwebinfo/cricket-api")

    # Step 2: Navigate to the Directory
    os.chdir("./cricket-api/api")

    # Step 3: Install the Dependencies
    run_command("python3 -m pip install -r requirements.txt")

    os.chdir("../../../../BOS")

def install_packages_from_requirements():
    """
    Install packages listed in requirements file.
    
    Args:
    requirements_file (str): Path to the requirements file.
    """
    requirements_file="../requirements.txt"
    setup_cricket_api()
    try:
        with open(requirements_file, 'r') as file:
            for line in file:
                package = line.strip()  # Remove whitespace and newline characters
                subprocess.run(["pip", "install", package], check=True)
        print("Packages installed successfully.")
    except Exception as e:
        print(f"Error installing packages: {e}")

# Example usage:

install_packages_from_requirements()
