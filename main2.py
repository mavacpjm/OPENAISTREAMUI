import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}
conversation_history = []

def generate_response(prompt):
    conversation_history.append(prompt)
    full_prompt = "\n".join(conversation_history)

    data = {"model": "mistral", "stream": False, "prompt": full_prompt}  # Enable streaming

    response = requests.post(url, headers=headers, stream=True, data=json.dumps(data))  # Stream response

    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024):  # Process chunks
            response_text = chunk.decode("utf-8")
            if response_text:  # Filter out empty chunks
                data = json.loads(response_text)
                actual_response = data.get("response", "")  # Handle partial responses
                conversation_history.append(actual_response)
                yield actual_response  # Yield partial responses for real-time rendering
    else:
        print("Error:", response.status_code, response.text)
        yield None

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    live=True,  # Enable live mode for real-time updates
    outputs="textbox",  # Use a textbox for real-time rendering
)

iface.launch()
