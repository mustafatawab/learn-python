import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig

@cl.on_message
async def main(message: cl.Message):
    await cl.Message(content=f"Recieved {message.content}").send()



@cl.on_chat_start
async def start():
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

    await cl.Message(content="Welcome to the Panaversity AI Assistant! How can I help you today?").send()
