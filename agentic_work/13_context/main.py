import asyncio
from multiprocessing import context
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, RunContextWrapper, function_tool
from dotenv import load_dotenv, find_dotenv
import os
from agents.run import RunConfig
from dataclasses import dataclass


load_dotenv()

gemini_key = os.environ.get("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("Please set gemini api 🔑 ")

@dataclass
class User:
    username:str
    email: str


@function_tool
def search(context: RunContextWrapper[User] , query : str) -> str:
    print(context.context)
    return ""

set_tracing_disabled(True)

client = AsyncOpenAI(api_key=gemini_key , base_url='https://generativelanguage.googleapis.com/v1beta/openai/')

llm_model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")

config = RunConfig(model=llm_model, model_provider=client)

agent = Agent(name="assitant" , instructions='you are helpful assistant',tools=[search])

user = User(username='Mustafa Tawab' , email='tawab05@gmail.com')

result = Runner.run_sync(agent, 'Hi, search the web for best LLMs', run_config=config, context=user)

print(result.final_output)