"""
ai_airline_assistant_multimodal.py
  Generates images using DALL-E 3 via the artist() function.
  Each image costs ~4 cents, so use sparingly!
"""

import base64
import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from openai import OpenAI
import json
import gradio as gr
from db import initialize_db, get_ticket_price

initialize_db()
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
  print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
  print("OpenAI API Key not set")

MODEL = "gpt-4.1-mini"
openai = OpenAI()

system_message = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}
tools = [{"type": "function", "function": price_function}]


def artist(city):
  image_response = openai.images.generate(
    model="dall-e-3",
    prompt=f"An image representing a vacation in {city}, showing tourist spots and everything unique about {city}, in a vibrant pop-art style",
    size="1024x1024",
    n=1,
    response_format="b64_json",
  )
  image_base64 = image_response.data[0].b64_json
  image_data = base64.b64decode(image_base64)
  return Image.open(BytesIO(image_data))

def talker(message):
  response = openai.audio.speech.create(
    model="gpt-4o-mini-tts",
    voice="onyx",  # Also, try replacing onyx with alloy or coral
    input=message
  )
  return response.content


#image = artist("New York City")
#image.show()


def chat(history):
  history = [{"role": h["role"], "content": h["content"]} for h in history]
  messages = [{"role": "system", "content": system_message}] + history
  response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)
  cities = []
  image = None

  while response.choices[0].finish_reason == "tool_calls":
    message = response.choices[0].message
    responses, cities = handle_tool_calls_and_return_cities(message)
    messages.append(message)
    messages.extend(responses)
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

  reply = response.choices[0].message.content
  history += [{"role": "assistant", "content": reply}]

  voice = talker(reply)

  if cities:
    image = artist(cities[0])

  return history, voice, image

def handle_tool_calls_and_return_cities(message):
  responses = []
  cities = []
  for tool_call in message.tool_calls:
    if tool_call.function.name == "get_ticket_price":
      arguments = json.loads(tool_call.function.arguments)
      city = arguments.get('destination_city')
      cities.append(city)
      price_details = get_ticket_price(city)
      responses.append({
        "role": "tool",
        "content": price_details,
        "tool_call_id": tool_call.id
      })
  return responses, cities


# Callbacks (along with the chat() function above)
def put_message_in_chatbot(message, history):
        return "", history + [{"role":"user", "content":message}]

# UI definition
with gr.Blocks() as ui:
    with gr.Row():
        chatbot = gr.Chatbot(height=500)
        image_output = gr.Image(height=500, interactive=False)
    with gr.Row():
        audio_output = gr.Audio(autoplay=True)
    with gr.Row():
        message = gr.Textbox(label="Chat with our AI Assistant:")

# Hooking up events to callbacks

    message.submit(put_message_in_chatbot, inputs=[message, chatbot], outputs=[message, chatbot]).then(
        chat, inputs=chatbot, outputs=[chatbot, audio_output, image_output]
    )

ui.launch(inbrowser=True, auth=("ed", "bananas"))

