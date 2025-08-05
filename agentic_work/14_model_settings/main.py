import asyncio
from pyexpat import model
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, ModelSettings, function_tool
from agents.run  import RunConfig
from dotenv import load_dotenv, find_dotenv
import os

_: bool = load_dotenv(find_dotenv())
set_tracing_disabled(True)
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Please set gemini api key")

@function_tool
def calculator(num1 : int , num2: int , op : str) -> float:
    """ Calculator of two operands """
    if op == "+":
        return float(num1 + num2)

    if op == "-":
        return float(num1 - num2)
    if op == "*":
        return float(num1 * num2)
    if op == "/":
        return float(num1 / num2)
    if op == "%":
        return float(num1 % num2)
    if op == "**":
        return float(pow(num1, num2))
    

client : AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

run_config: RunConfig = RunConfig(
    model=OpenAIChatCompletionsModel(openai_client=client, model='gemini-2.0-flash'),
    model_provider=client
)

agent_cold: Agent = Agent(name='cold_agent' , instructions='you are helpful assistant' , model_settings=ModelSettings(temperature=1.9 , tool_choice='auto') , tools=[calculator])
agent_hot: Agent = Agent(name='hot_agent' , instructions='you are helpful assistant' , model_settings=ModelSettings(temperature=0.1 , tool_choice='none'), tools=[calculator])


async def main():
    result : Runner = await Runner.run(agent_hot , "what is 100 + 90", run_config=run_config)
    print(result.final_output)

asyncio.run(main())

