import chainlit as cl # type: ignore
from agents import Agent, RunConfig , AsyncOpenAI , OpenAIChatCompletionsModel, Runner #type: ignore
from dotenv import load_dotenv , find_dotenv #type: ignore
import os

load_dotenv(find_dotenv())


gemini_api_key = os.getenv("GEMINI_API_KEY")


provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)



model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)


run_config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled=True
)


agent = Agent(
    instructions="You are helpful assitant  than can answer questions",
    name='General Assistant'
)


# result = Runner.run_sync(
#     agent,
#     input='What is the capital of Pakistan',
#     run_config=run_config,
    
# )


# print(result)

@cl.on_chat_start
async def hamndle_chat_start():
    cl.user_session.set("history" , []),
    await cl.Message(content="I am general assistant").send()


@cl.on_message
async def handle_message(message : cl.Message):
    history = cl.user_session.get("history")

    history.append({
        "role" : "user",
        "content" : message.content
    })
    result = await Runner.run(
        agent,
        input=history,
        run_config=run_config
    )


    history.append({
        "role" : "user",
        "content" : result.final_output
    })
    await cl.Message(content=f"Hello {result.final_output}").send()


