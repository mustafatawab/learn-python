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

@function_tool
def get_weather(location: str) -> str:
    # Simulate a weather API call
    return f"The weather in {location} is sunny with a high of 25°C."


base_agent: Agent = Agent(
    name="base_agent",
    model=llm_model,
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    tools=[get_current_time],
    model_settings=ModelSettings(
        temperature=0.9,
    )
)


agents = {
    "Creative Agent" : base_agent.clone(
        name="creative_agent",
        instructions="You are a creative assistant that can help with artistic tasks.",
        model_settings=ModelSettings(temperature=0.7),
    ),

    "Analytical Agent" : base_agent.clone(
        name="analytical_agent",
        instructions="You are an analytical assistant that can help with data analysis.",
        model_settings=ModelSettings(temperature=0.3),
    ),
    "Weather Agent" : base_agent.clone(
        name="weather_agent",
        instructions="You are a weather assistant that can provide weather updates.",
        tools=[get_weather],
        model_settings=ModelSettings(temperature=0.5),
    )
}

prompt = "HI, tell me about AGENTIC AI"
for name , agent  in agents.items():
    result = Runner.run_sync(
        agent,
        prompt
    )
    print("-----------------")
    print(f"Result from {name}: {result.final_output}")