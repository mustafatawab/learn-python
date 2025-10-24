from agents import Agent, Runner, AsyncOpenAI,handoff, OpenAIChatCompletionsModel, function_tool, RunContextWrapper # pyright: ignore[reportMissingImports]
from agents.run import RunConfig # type: ignore
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

gemini_api_key: str = os.environ.get("GEMINI_API_KEY") 

if not gemini_api_key:
    raise ValueError('GEMINI API key is not set properly')

client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'

)


model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash"
)

run_config: RunConfig = RunConfig(
    model=model,
    model_provider=client
)

@function_tool
def get_weather(city: str) -> str:
    """ Use this tool for the weather information """
    return f"The weatheri in {city} is 22 C"

class WeatherRequest(BaseModel):
    location: str
    temperature : str
    extra_info : dict | None = None



def on_weather_transfer(context: RunContextWrapper , input : WeatherRequest):
    print("\n Handoff to the weather agent \n" , input)


search_agent: Agent = Agent(
    name='search_agent',
    instructions='You are search agent. You search the user query get nice response in a short way.'
)

weather_agent: Agent = Agent(
    name='weather_agent',
    instructions='You are weather agent and responsible only for the weather information.',
    tools=[get_weather]
)

agent: Agent = Agent(
    name='orchestrator',
    instructions='You are helpful assistant. Always transfer the user query to weather_agent for the weather query and search_agent for the searching ',
    handoffs=[handoff(weather_agent, on_handoff=on_weather_transfer) , handoff(search_agent)]
)


result: Runner = Runner.run_sync(
    agent,
    "Hi, what is the weather in Karachi",
    run_config=run_config,
    max_turns=15
)


print(result.final_output)