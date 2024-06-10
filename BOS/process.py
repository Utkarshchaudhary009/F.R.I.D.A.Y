import requests

def process(command):
    try:
        response = requests.post("http://localhost:5000/api/process", json={"command": command})
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        try:
            return response.json()  # Attempt to parse JSON response
        except requests.exceptions.JSONDecodeError:
            print(f"Error decoding JSON. Response text: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
        return {"response":f"HTTP request error: { 'INTERNAL SERVER ERROR' if '500' in  '<Response [500]>' else e.response }"}

if __name__ == "__main__":
    result = process("hello jarvis")
    print(result)
