"""
LLM Client with simple chat method and stream chat method.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

llm_model = "gpt-4o-mini"
llm_temp = 0.3

class LLMClient:
    @staticmethod 
    def chat(messages, temperature=llm_temp): 
        response = client.chat.completions.create( 
            model=llm_model, 
            messages=messages, 
            temperature=temperature 
        ) 
        return response.choices[0].message.content
    
    @staticmethod
    def stream_chat(messages, temperature=llm_temp):
        stream = client.chat.completions.create(
            model=llm_model,
            messages=messages,
            stream=True
        )

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta