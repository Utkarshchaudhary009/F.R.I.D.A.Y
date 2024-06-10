import subprocess

def install_packages_from_requirements():
    """
    Install packages listed in requirements file.
    
    Args:
    requirements_file (str): Path to the requirements file.
    """
    requirements_file="../requirements.txt"
    try:
        with open(requirements_file, 'r') as file:
            for line in file:
                package = line.strip()  # Remove whitespace and newline characters
                subprocess.run(["pip", "install", package], check=True)
        print("Packages installed successfully.")
    except Exception as e:
        print(f"Error installing packages: {e}")

# Example usage:

#install_packages_from_requirements("requirements.txt")
