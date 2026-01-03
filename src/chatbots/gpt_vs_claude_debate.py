"""
    This application simulates a dynamic debate between two large language models (LLMs) 
		on the topic of student loan repayment, with each model representing opposing viewpoints. 
		The goal is to provide an engaging, interactive experience that helps users explore 
		both sides of this complex issue.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load OpenAI API key
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")

# Initialize OpenAI API
openai = OpenAI()

# Model and system messages
gpt_model = "gpt-4.1-mini"
claude_model = "claude-3-5-haiku-latest"

gpt_system = "You are a chatbot in a debate and  who favors Loan forgiveness for students who have no way ; \
of paying their loans."

claude_system = "You are a chatbot in a debate  who does not favor Loan forgiveness for all students \
no matter what their socio-economic status.  For you a loan is a loan that needs to be, \
repaid."

# Initial messages
gpt_messages = ["Hi there"]
claude_messages = ["Hi"]

"""
    Uses OpenAPI LLM
"""
def call_gpt():
    """Send messages to GPT and return its response."""
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, claude in zip(gpt_messages, claude_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": claude})
    response = openai.chat.completions.create(model=gpt_model, messages=messages)
    return response.choices[0].message.content

"""
    If we have a Claude subscription we can use Claude LLM
        For now use OpenAPI LLM
"""
def call_claude():
    """Send messages to Claude and return its response."""
    messages = [{"role": "system", "content": claude_system}]
    for gpt, claude_message in zip(gpt_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": claude_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    response = openai.chat.completions.create(model=gpt_model, messages=messages)
    return response.choices[0].message.content

if __name__ == "__main__":
		# Start debates
    gpt_messages = ["Hi there"]
    claude_messages = ["Hi"]

    print(f"### GPT:\n{gpt_messages[0]}\n")
    print(f"### Claude:\n{claude_messages[0]}\n")

		# Simulate debate for 5 rounds
    for i in range(5):
        gpt_next = call_gpt()
        print(f"### GPT:\n{gpt_next}\n")
        gpt_messages.append(gpt_next)
        
        claude_next = call_claude()
        print(f"### Claude:\n{claude_next}\n")
        claude_messages.append(claude_next)
