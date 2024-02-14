import requests
import json
import time

def generate_prompt_response(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "mistral",
        "stream": False,
        "prompt": prompt,
    }
    
    try:
        response = requests.post(url, json=data, stream=True)
        response.raise_for_status()  # Raise an error for bad response status
        
        # Parse JSON response and extract text
        response_json = response.json()
        generated_text = response_json.get("response", "")
        
        # Split the text into words
        words = generated_text.split()

        # Print each word with a slight delay for real-time streaming effect
        for word in words:
            print(word, end=' ', flush=True)
            time.sleep(0.1)  # Adjust the delay as needed for desired speed
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    prompt = input("Enter prompt: ")
    generate_prompt_response(prompt)
