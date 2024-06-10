import os
import subprocess
import sys
from time import sleep
def install_ollama():
    try:
        # Check if Ollama is installed
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if "ollama" in result.stdout:
            print("Ollama is already installed.")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        # Install Ollama if not present
        print("Ollama is not installed. Installing Ollama...")
        subprocess.run([sys.executable, "-m", "pip", "install", "ollama"], check=True)

def install_model(model_name):
    try:
        # Check if the model is installed
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if model_name in result.stdout:
            print(f"{model_name} model is already installed.")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        # Pull the model if not present
        print(f"{model_name} model is not installed. Installing {model_name} model...")
        subprocess.run(["ollama", "pull", model_name], check=True)

def run_chatbot():
    import ollama

    print("Starting the chatbot with Phi and Orca-mini models...")

    # 50 sample user inputs for testing
    test_inputs = [
        "Tell me a joke",
        "What is the sum of 46 and 99?",
        "Why use Python to print even numbers till 50?",
        "Who killed Akbar?",
        "Write Python code to print only even numbers till 50.",
        "Explain the theory of relativity.",
        "What is the capital of France?",
        "How do I make a website?",
        "Tell me a fun fact.",
        "What is the square root of 144?",
        "Who is the president of the United States?",
        "What is the largest planet in our solar system?",
        "How do I change a tire?",
        "What are the benefits of exercise?",
        "What is the Pythagorean theorem?",
        "Describe the water cycle.",
        "Explain machine learning.",
        "What is photosynthesis?",
        "How do I set up a VPN?",
        "What is quantum computing?",
        "How do I cook spaghetti?",
        "What is the speed of light?",
        "Who wrote 'To Kill a Mockingbird'?",
        "What is the boiling point of water?",
        "How does a computer work?",
        "What are the symptoms of COVID-19?",
        "How can I improve my public speaking skills?",
        "What is the history of the Internet?",
        "How do I write a resume?",
        "What is the Fibonacci sequence?",
        "Who discovered penicillin?",
        "How do I create a Python virtual environment?",
        "What are the different types of clouds?",
        "How does the stock market work?",
        "What is blockchain technology?",
        "How do I start a garden?",
        "What is the function of the heart?",
        "Explain the law of supply and demand.",
        "What are the stages of cell division?",
        "How do I backup my data?",
        "What is artificial intelligence?",
        "Who painted the Mona Lisa?",
        "How do I build a mobile app?",
        "What is the formula for calculating interest?",
        "What are the Seven Wonders of the World?",
        "How do I meditate?",
        "What is the human genome project?",
        "How do I use Git for version control?",
        "What is climate change?"
    ]

    for user_input in test_inputs:
        print(f"\nYou: {user_input}")

        print("phi:")
        stream_phi = ollama.chat(
            model='phi',
            messages=[{'role': 'user', 'content': user_input}],
            stream=True,
        )
        for chunk in stream_phi:
            print(chunk['message']['content'], end='', flush=True)

        print("\norca-mini:")
        stream_orca = ollama.chat(
            model='orca-mini',
            messages=[{'role': 'user', 'content': user_input}],
            stream=True,
        )
        for chunk in stream_orca:
            print(chunk['message']['content'], end='', flush=True)
        print()
        sleep(20)

if __name__ == "__main__":
    install_ollama()
    install_model('phi')
    install_model('orca-mini')
    run_chatbot()
