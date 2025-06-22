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





@cl.on_chat_start
async def handle_chat_start() -> None:
    cl.user_session.set("history" , []),
    await cl.Message(content="I am general assistant").send()


@cl.on_message
async def send_message(message: cl.Message) -> None:
    history = cl.user_session.get("history")

    msg = cl.Message(content="")
    await msg.send()

    history.append({
        "role" : "user",
        "content" : message.content
    })

    print(history)
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
            "content": history
          }
        ]
      })
    )

    # Input must have atleast one token
    data  = response.json()
    print(data)

    history.append({
        "role" : "assistant",
        "content" : data['choices'][0]['message']['content']
    })

    cl.user_session.set("history" , history)



