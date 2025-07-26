from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Please add gemini api key")

client = OpenAI(api_key=api_key , base_url='https://generativelanguage.googleapis.com/v1beta/openai/')

def generate(content: str) ->str:

    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role" : "system" , "content" : "You are general assistant"},
            {"role" : "user" , "content" : content},
        ]
    )

    result = response.choices[0].message.content
    return result

print(generate("Hi"))