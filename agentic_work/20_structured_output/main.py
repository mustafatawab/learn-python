from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os


load_dotenv()
gemini_api_key: str = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Please set the GEMINI_API_KEY  key")


client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=client
)


@function_tool
def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny. It is 20C"

class ExtraData(BaseModel):
    humidity: str
    sources : list | str

class WeatherData(BaseModel):
    location: str | None = Field(default=None, description="location  ")
    temperature: str | None = Field(default=None, description='Temperature of the city')
    extra_info : ExtraData

agent = Agent(
    name='weather_agent',
    instructions='you get weather info',
    model=model,
    output_type=WeatherData
)


result = Runner.run_sync(
    agent,
    "What is weather in lohore"
)

print(result.final_output)


