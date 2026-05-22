"""
LLM Client with simple chat method.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

class LLMClient:
    @staticmethod 
    def chat(messages, temperature=0.3): 
        response = client.chat.completions.create( 
            model="gpt-4o-mini", 
            messages=messages, 
            temperature=temperature 
        ) 
        return response.choices[0].message.content