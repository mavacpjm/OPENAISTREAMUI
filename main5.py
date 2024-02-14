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
                if parsing_response:
                    if char == '}':
                        response_buffer += char
                        response_json = json.loads(response_buffer)
                        generated_text = response_json.get("response", "")
                        for word in generated_text.split():
                            for ch in word:
                                print(ch, end='', flush=True)
                                # Adjust delay here if needed
                            print(' ', end='', flush=True)  # Add space between words
                        parsing_response = False
                        response_buffer = ''
                    else:
                        response_buffer += char
                elif char == '{' and response_buffer == '':
                    parsing_response = True
                    response_buffer += char
    except requests.exceptions.RequestException as e:
        print("Error:", e)

if __name__ == "__main__":
    prompt = input("Enter prompt: ")
    generate_prompt_response(prompt)
