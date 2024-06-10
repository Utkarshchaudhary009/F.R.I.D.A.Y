import requests
from wiki import get_google_knowledge_graph
def wolframalpha_response(query):
    try:
        app_id = "V4PV3Y-R225H6TVL7"  # Replace with your actual WolframAlpha App ID

        if not query:
            return {"response": "No query provided for WolframAlpha"}

        url = "http://api.wolframalpha.com/v1/result"
        params = {
            'i': query,
            'appid': app_id,
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            result = response.text.strip()
            return {"response": result}
        else:
            return {"response":get_google_knowledge_graph(query)["response"]}

    except Exception as e:
        return {"response": f"Sorry, an error occurred: {str(e)}"}

# Example usage
if __name__=="__main__":
    print(wolframalpha_response("tell me a joke"))
