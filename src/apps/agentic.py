import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from db import initialize_db, get_ticket_price


load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
  print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
  print("OpenAI API Key not set")

MODEL = "gpt-4.1-mini"
openai = OpenAI()

initialize_db()
print(get_ticket_price("london"))