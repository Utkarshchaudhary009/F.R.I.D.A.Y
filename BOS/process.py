import requests

def process(command):
    response = requests.post("http://localhost:5000/api/process", json={"command": command})
    return response.json()
