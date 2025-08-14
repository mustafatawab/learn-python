from agents import Agent, Runner, AsyncOpenAI , OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, ModelSettings

from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")


client: AsyncOpenAI = AsyncOpenAI(api_key=gemini_api_key , base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client,
)

@function_tool
def get_current_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

original_agent: Agent = Agent(
    name="base_agent",
    model=llm_model,
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    tools=[get_current_time],
    model_settings=ModelSettings(
        temperature=0.9,
    )
)

variants = {
    "scientist" : original_agent.clone(
        name='scientist_agent',
        instructions="You are a scientist that can help with scientific inquiries.",
    ),

    "artist" : original_agent.clone(
        name='artist_agent',
        instructions="You are an artist that can help with creative tasks.",
    ),

    "poet" : original_agent.clone(
        name='poet_agent',
        instructions="You are a poet that can help with writing poetry.",
    ),

    "chef" : original_agent.clone(
        name='chef_agent',
        instructions="You are a chef that can help with cooking recipes.",
    )
}


for name, agent in variants.items():
    response: Runner =  Runner.run_sync(
        agent,
        f"Hello {name}, can you tell me what is your name and how you feel today? Also, please let me know the current time."
     )
    
    print(f"Response from {name}: {response.final_output}")
    print("-----------------")