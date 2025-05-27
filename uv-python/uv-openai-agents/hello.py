import chainlit as cl # type: ignore
from agents import WebSearchTool,Agent, RunConfig , AsyncOpenAI , OpenAIChatCompletionsModel, Runner, function_tool #type: ignore
from dotenv import load_dotenv , find_dotenv #type: ignore
from openai.types.responses import ResponseTextDeltaEvent # type: ignore
import os
import random


load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

@function_tool("get_weather")
def get_weather(location : str) -> str:

    """" 
        Find the weather of given location in Degree Calcius or something like this
    """
    return f"the weather of {location}  is 22 degree"

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
    name='General Assistant',
    tools=[get_weather]
)


# result = Runner.run_sync(
#     agent,
#     input='What is the capital of Pakistan',
#     run_config=run_config,
    
# )


# print(result)





@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history" , []),
    await cl.Message(content="I am general assistant").send()


@cl.on_message
async def handle_message(message : cl.Message):
    history = cl.user_session.get("history")

    msg = cl.Message(content="")
    await msg.send()

    history.append({
        "role" : "user",
        "content" : message.content
    })
    # result = await Runner.run(
    #     agent,
    #     input=history,
    #     run_config=run_config
    # )
    result = Runner.run_streamed(agent, input=history, run_config=run_config)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            # print(event.data.delta, end="", flush=True)
            await msg.stream_token(event.data.delta)

    history.append({
        "role" : "assistant",
        "content" : result.final_output
    })
    cl.user_session.set("history" , history)
    # await cl.Message(content=f"Hello {result.final_output}").send()


