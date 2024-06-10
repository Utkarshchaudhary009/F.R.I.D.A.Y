# Friday\utils\readEnv.py
import os
from dotenv import load_dotenv
import sys
# Add parent directory to sys.path to make absolute imports work
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(parent_dir)
if parent_dir not in sys.path:
    sys.path.append(f"{parent_dir}/utilities")

def readEnv(variable):
    # Assuming the .env file is in the parent directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '../data/api.env')
    #print(dotenv_path)
    load_dotenv(dotenv_path)
    vardata = os.getenv(variable)
    #print(vardata)
    return vardata
# Example usage
if __name__ == "__main__":
    readEnv("NEWS")