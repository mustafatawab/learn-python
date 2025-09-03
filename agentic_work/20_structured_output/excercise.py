from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool
from agents.run import RunConfig
from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key: str = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Your API key is not in the env or not loaded")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client,
    model='gemini-2.0-flash'
)

