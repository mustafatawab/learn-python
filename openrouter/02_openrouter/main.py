import os
from dotenv import load_dotenv
import nest_asyncio
import requests
import json
import chainlit as cl


nest_asyncio.apply()
_:bool = load_dotenv()

BASE_URL = "https://openrouter.ai/api/v1"   
MODEL = "mistralai/mistral-small-3.2-24b-instruct:free"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")



response = requests.post(
  url=f"{BASE_URL}/chat/completions",
  headers={
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
  },
  data=json.dumps({
    "model": MODEL,
    "messages": [
      {
        "role": "user",
        "content": "what do you think about the my personal software agency. The name is Farsight Systems. "
      }
    ]
  })
)


@cl.on_message
async def send_message(msg: cl.Message) -> None:
    await cl.Message(
        content=f"I received {msg.content} from the user"
    ).send()



