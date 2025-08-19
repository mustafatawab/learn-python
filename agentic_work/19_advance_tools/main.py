from agents import AsyncOpenAI, OpenAIChatCompletionsModel , Agent, Runner, function_tool, RunContextWrapper, ItemHelper
from agents.type.responses import ResponseTextDeltaEvent
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