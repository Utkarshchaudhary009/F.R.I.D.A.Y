import subprocess
import os
import sys

def create_venv(env_name):
    """
    Create a virtual environment with the specified name.
    """
    try:
        os.chdir("F:/")
        print(f"Current directory: {os.getcwd()}")
        subprocess.run(['python', '-m', 'venv', env_name], check=True)
        print(f"Virtual environment '{env_name}' created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")

def get_venv_python(env_name):
    """
    Get the path to the virtual environment's Python interpreter.
    """
    return os.path.join(env_name, 'Scripts', 'python.exe')

def install_dependencies(venv_python):
    """
    Install dependencies using the virtual environment's Python interpreter.
    """
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "-r", "F:/Friday/requirements.txt"], check=True)
        subprocess.run([venv_python, "-m", "spacy", "download", "en_core_web_sm"], check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")

def check_venv_activated():
    """
    Check if the virtual environment is activated.
    """
    return sys.prefix != sys.base_prefix

def verify_packages(venv_python, required_packages):
    """
    Verify that the required packages are installed.
    """
    try:
        installed_packages = subprocess.run([venv_python, '-m', 'pip', 'list'], capture_output=True, text=True, check=True)
        installed_packages_list = installed_packages.stdout
        for package in required_packages:
            if package not in installed_packages_list:
                return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error verifying packages: {e}")
        return False

def deactivate_venv():
    """
    Deactivate the currently activated virtual environment.
    """
    try:
        os.chdir("F:/")
        print(f"Current directory: {os.getcwd()}")
        os.system('deactivate')
        print("Virtual environment deactivated.")
    except Exception as e:
        print(f"Error deactivating virtual environment: {e}")

if __name__ == "__main__":
    venv_path = "Friday/venv"
    create_venv(venv_path)
    venv_python = get_venv_python(venv_path)
    
    install_dependencies(venv_python)
    
    if check_venv_activated():
        print("Virtual environment is activated.")
    else:
        print("Virtual environment is not activated.")
    
    required_packages = ['requests', 'pyaudio', 'SpeechRecognition', 'pyttsx3', 'spacy']
    if verify_packages(venv_python, required_packages):
        print("All required packages are installed.")
    else:
        print("Some required packages are missing.")
    
    # Here you can add your user configuration code if needed
    # For example:
    # setup_configuration()
    
    deactivate_venv()
    print("Setup complete.")
