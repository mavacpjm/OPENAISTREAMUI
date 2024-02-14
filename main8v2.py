import requests
import gradio as gr
import json

url = "http://localhost:11434/api/generate"

def generate_response(prompt):
    response = requests.post(url, json={"model": "mistral", "stream": True, "prompt": prompt}, stream=True)
    
    accumulated_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if "response" in data:
                response_text = data["response"]
                # Check if the accumulated response ends with a space, and if the new response starts with one
                if accumulated_response.endswith(" ") and response_text.startswith(" "):
                    accumulated_response += response_text[1:]  # Add the response without the initial space
                else:
                    accumulated_response += response_text
                yield accumulated_response
            if "done" in data and data["done"]:
                break

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text",
    title="Real-time JSON Response Display"
)

iface.launch()
