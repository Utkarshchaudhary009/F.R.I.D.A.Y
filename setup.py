# setup.py
from setuptools import setup, find_packages
from Brain.data.scripts.userSetup import user_setup
from BOS.Install_dependencies import install_packages_from_requirements
import subprocess
import os

# Install dependencies for BOS package
# subprocess.run(["pip", "install", "-e", "./BOS"])
# subprocess.run(["pip", "install", "-e", "./Brain/services"])
print("\n\n done \n\n")
if __name__ == "__main__":
    install_packages_from_requirements()
    user_setup()
    print("Setup complete.")

# Define your setup parameters
setup(
    name='Friday',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pyttsx3',
        'spacy',
        'requests',
        'pyjokes',
        'Flask',
    ],
)

