import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, SQLiteSession
from dotenv import load_dotenv
import os
from typing import cast


load_dotenv()

gemini_api_key: str = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI API KEY is not yet set properly..... ")

@cl.on_chat_start
async def chat_start():

    client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    model = OpenAIChatCompletionsModel(
        model='gemini-2.5-flash',
        openai_client=client
    )

    agent = Agent(
        name='general_assistant',
        instructions='You are general assistant.',
        model=model
    )

    cl.user_session.set("agent" , agent)
    cl.user_session.set("chat_history" , [])



@cl.on_message
async def main(message: cl.Message):

    msg = cl.Message(content="")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    
    history = cl.user_session.get("chat_history") or []

    history.append(
        {"role" : "user", "content" : message.content}
    )

    result = Runner.run_sync(
        agent,
        history
    )

    msg.content = result.final_output
    await msg.send()


    cl.user_session.set("chat_history" , result.to_input_list())

# @cl.on_chat_start
# async def start():
    #Reference: https://ai.google.dev/gemini-api/docs/openai
    # external_client = AsyncOpenAI(
    #     api_key=gemini_api_key,
    #     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    # )

    # model = OpenAIChatCompletionsModel(
    #     model="gemini-2.0-flash",
    #     openai_client=external_client
    # )

    # config = RunConfig(
    #     model=model,
    #     model_provider=external_client,
    #     tracing_disabled=True
    # )
    # """Set up the chat session when a user connects."""
    # # Initialize an empty chat history in the session.
    # cl.user_session.set("chat_history", [])

    # cl.user_session.set("config", config)
    # agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)
    # cl.user_session.set("agent", agent)

    # await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()
