import requests
import json
from gtts import gTTS
from tempfile import TemporaryFile
import subprocess
import gradio as gr

url = "http://localhost:11434/api/generate"

def generate_response(prompt):
    response = requests.post(url, json={"model": "mistral", "stream": True, "prompt": prompt}, stream=True)
    
    accumulated_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if "response" in data:
                response_text = data["response"]
                if accumulated_response.endswith(" ") and response_text.startswith(" "):
                    accumulated_response += response_text[1:]
                else:
                    accumulated_response += response_text
                # Generate speech from the accumulated response
                tts = gTTS(text=accumulated_response, lang='en')
                with TemporaryFile() as f:
                    tts.write_to_fp(f)
                    f.seek(0)
                    # Play the speech using the default audio player
                    subprocess.Popen(["ffplay", "-autoexit", "-nodisp", "-"], stdin=f)
                return accumulated_response

iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
    outputs=gr.Textbox(label="Response"),
    title="Real-time JSON Response Display with Text-to-Speech",
    allow_flagging=False,
    
)

iface.launch()
