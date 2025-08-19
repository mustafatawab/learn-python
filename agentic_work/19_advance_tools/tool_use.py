from agents import AsyncOpenAI, OpenAIChatCompletionsModel , Agent, Runner, function_tool, RunContextWrapper, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import asyncio
import os
from agents.run import RunConfig

# Load environment variables from .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    client=client,
    model="gemini-1.5-flash",
)

@function_tool
def get_current_time() -> str:
    """Returns the current time in ISO format."""
    from datetime import datetime
    return datetime.now().isoformat()

@function_tool
def get_weather(location: str) -> str:
    """Returns the current weather for a given location."""
    # Placeholder implementation
    return f"The current weather in {location} is sunny with a temperature of 25°C."


agent :Agent = Agent(
    name='helpful_agent',
    instructions="You are a helpful assistant that can answer questions and perform tasks.",
    model=model,
    tools=[get_current_time, get_weather],
)

async def main() -> None:
    result: Runner = await Runner.run(
        agent, 
        "What current time and wather in Pakistan"
    )

    print(result.final_output)

asyncio.run(main())