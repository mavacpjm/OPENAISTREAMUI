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
                words = response_text.split()
                for word in words:
                    accumulated_response += word + " "
                    yield accumulated_response.strip()
            if "done" in data and data["done"]:
                break

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs="text",
    title="Real-time JSON Response Display"
)

iface.launch()
