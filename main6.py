import requests
import json
import sys

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

        # Variables to keep track of response parsing
        parsing_response = False
        response_buffer = ''
        
        # Process the response character by character
        for byte in response.iter_content(chunk_size=1):
            if byte:
                char = byte.decode('utf-8')
                
                # Accumulate characters only if parsing_response is True
                if parsing_response:
                    response_buffer += char
                    # Check if the end of JSON object is reached
                    if char == '}':
                        response_json = json.loads(response_buffer)
                        generated_text = response_json.get("response", "")
                        print(generated_text, end='', flush=True)
                        # Check if "done": true is observed
                        if response_json.get("done", False):
                            break  # End processing if "done": true is observed
                        response_buffer = ''  # Reset buffer for next JSON object
                elif char == '{':
                    parsing_response = True
                    response_buffer = char
                
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    prompt = input("Enter prompt: ")
    generate_prompt_response(prompt)

