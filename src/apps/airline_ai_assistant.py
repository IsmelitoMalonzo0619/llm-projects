import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

def init_openai() :
  load_dotenv(override=True)

  openai_api_key = os.getenv('OPENAI_API_KEY')
  if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
  else:
    print("OpenAI API Key not set")

  MODEL = "gpt-4.1-mini"
  openai = OpenAI()

def get_ticket_price(destination_city):
  ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

  print(f"Tool called for city {destination_city}")
  price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
  return f"The price of a ticket to {destination_city} is {price}"

def handle_tool_calls(message):
  responses = []
  for tool_call in message.tool_calls:
    if tool_call.function.name == "get_ticket_price":
      arguments = json.loads(tool_call.function.arguments)
      city = arguments.get('destination_city')
      price_details = get_ticket_price(city)
      responses.append({
        "role": "tool",
        "content": price_details,
        "tool_call_id": tool_call.id
      })
  return responses

''' 
  call back function for Gradio 
    message - what is asked in the message box
    history - conversation history of user and LLM (content in the UI)
'''
def chat(message, history):
  if history is None:
    history = []
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

  history = [{"role": h["role"], "content": h["content"]} for h in history]
  messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
  response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

  while response.choices[0].finish_reason == "tool_calls":
    message = response.choices[0].message
    responses = handle_tool_calls(message)
    messages.append(message)
    messages.extend(responses)
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

  return response.choices[0].message.content



gr.ChatInterface(fn=chat, type="messages").launch()
