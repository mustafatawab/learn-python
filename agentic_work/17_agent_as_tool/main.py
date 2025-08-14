from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from dotenv import load_dotenv

import os

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")


external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)


llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash"
)


agent: Agent = Agent(
    name="agent",
    model=llm_model,
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
)

result: Runner = Runner.run_sync(
    agent,
    "Hi, What is your name and how you feel today?"
)

print(result.final_output)