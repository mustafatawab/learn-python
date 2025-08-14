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

base_agent: Agent = Agent(
    name="base_agent",
    model=llm_model,
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    tools=[get_current_time],
    model_settings=ModelSettings(
        temperature=0.9,
    )
)



cloned_agent = base_agent.clone(
    name="cloned_agent",
    model_settings=ModelSettings(temperature=0.1)
)


result: Runner = Runner.run_sync(
    base_agent,
    "Hi, What is your name and how you feel today? also lemme know What is current time"
)

result1: Runner = Runner.run_sync(
    cloned_agent,
    "Hi, What is your name and how you feel today? also lemme know What is current time. "
)

print("-----------------")
print(result.final_output)
print("-----------------")
print(result1.final_output)
print("-----------------")
# print(base_agent.tools[0].name)
# print(cloned_agent.tools[0].name)