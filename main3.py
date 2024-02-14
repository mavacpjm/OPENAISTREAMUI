import requests

def generate_prompt_response(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "mistral",
        "stream": True,
        "prompt": prompt,
    }
    
    try:
        response = requests.post(url, json=data, stream=True)
        response.raise_for_status()  # Raise an error for bad response status
        
        # Parse JSON response and extract text
        response_json = response.json()
        generated_text = response_json.get("response", "")
        
        print(generated_text)  # Print generated text
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    prompt = input("Enter prompt: ")
    generate_prompt_response(prompt)


