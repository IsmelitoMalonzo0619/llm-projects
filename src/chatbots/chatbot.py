"""
    This is a simple conversational chatbot.
		It uses Gradio for UI
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr # for the UI

# Load OpenAI API key
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")

# Initialize OpenAI API
openai = OpenAI()
MODEL = 'gpt-4.1-mini'

system_message = "You are a physics assistant. You are to solve problems that physics students encounters \
in their  homework.  Make sure that you provide brief explanation and response to their additional questions."

def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history]
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    stream = openai.chat.completions.create(model=MODEL, messages=messages, stream=True)
    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response


if __name__ == "__main__":
    print("Starting the chatbot...")
    gr.Interface(fn=chat, inputs=["text", "text"], outputs="text").launch()
    print("Ending the chatbot...")
