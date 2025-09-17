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
class TravelContext:
    name: str = "mustafa"
    tone: str = "friendly"
    destination: str = 'islamabad'

    def dynamic_instructions(self):
        
        return (
            f"""you are a {self.tone} travel agent
            the user name is {self.name}
            provide personalize travel suggestions ideally for {self.destination}
            keep the result and short and concise"""
        )


@function_tool
def search(context: RunContextWrapper[TravelContext] , query : str) -> str:
    print(context.context)
    return ""

set_tracing_disabled(True)

travel = TravelContext(
    name=input("Enter your name"),
    tone=input("which tone would you like the agent to respond to you "),
    destination=input("what is your destination to go for travel ")
)

client = AsyncOpenAI(api_key=gemini_key , base_url='https://generativelanguage.googleapis.com/v1beta/openai/')

llm_model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")

config = RunConfig(model=llm_model, model_provider=client)

agent = Agent(name="assitant" , instructions=travel.dynamic_instructions(), tools=[search])


while True:
    user_input = input("\n Ask me anything about your trip ? (exit) for exit \n")
    if user_input == 'exit':
        break

    result = Runner.run_sync(agent, user_input, run_config=config, context=travel)

    print(result.final_output)