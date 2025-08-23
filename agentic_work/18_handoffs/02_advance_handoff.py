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
    return "Calling weather function about " + city

class NewsRequest(BaseModel):
    topic: str
    reason: str

def on_news_transfer(ctx: RunContextWrapper , input_data:NewsRequest):
    print("transferring to News Agent : Input Data" , input_data)



search_agent: Agent = Agent(
    name='search_agent',
    instructions='You are search agent. You search the user query get nice response in a short way.'
)

news_agent: Agent = Agent(
    name='news_agent',
    instructions='You get latest news about Tech community.'
)

agent: Agent = Agent(
    name='orchestrator',
    instructions='You are orchestor and you have the control over all agent. You itself will not response the user but transefer to the other agents.',
    handoffs=[handoff(agent=news_agent, on_handoff=on_news_transfer , input_type=NewsRequest) , handoff(search_agent)]
)


result: Runner = Runner.run_sync(
    agent,
    "What the hot technology in IT industry right now?",
    run_config=run_config
)


print(result.final_output)