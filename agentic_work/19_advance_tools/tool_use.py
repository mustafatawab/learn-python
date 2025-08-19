from agents import ModelSettings, AsyncOpenAI, OpenAIChatCompletionsModel ,StopAtTools, Agent, Runner, function_tool, RunContextWrapper, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import asyncio
import os

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
    openai_client=client,
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



@function_tool
def web_search(query: str) -> str:
    """ Perform web search over the internet"""
    return f"The user asks about {query}"

agent :Agent = Agent(
    name='helpful_Assistant',
    instructions="You are a helpful assistant that can answer questions and perform tasks.",
    model=model,
    model_settings=ModelSettings(
                temperature=0.8, 
                tool_choice="required", # tool_choice -> required, auto, none
                max_tokens=300,
                # parallel_tool_calls=True
                ), 
    tools=[get_weather, web_search, get_current_time],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_weather", "web_search"]) # run_llm_again , stop_on_first_tool, StopAtTools(stop_at_tool_names=["your_tool"])
)

async def main() -> None:
    result: Runner = await Runner.run(
        agent, 
        "Can you please search best agentic ai tools? Also lemme know what is the weather in Tokyo right now. Try it atleast 5 times",
        max_turns=1
    )

    print(result.final_output)

asyncio.run(main())