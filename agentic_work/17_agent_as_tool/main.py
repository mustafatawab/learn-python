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


scientis_agent: Agent = Agent(
    name='scientist',
    model=llm_model,
    instructions="You are a scientist that can answer questions and help with tasks.",
)


agent: Agent = Agent(
    name="agent",
    model=llm_model,
    instructions="You are a helpful assistant that can answer questions and help with tasks.",
    tools=[scientis_agent.as_tool(
        tool_name="scientist_tool",
        tool_description="A tool that can answer questions and help with tasks.",
    )]
)

result: Runner = Runner.run_sync(
    agent,
    "Hi, Can you please research on modern web technologies and their impact on the future of the web?"
)

print(result.final_output)