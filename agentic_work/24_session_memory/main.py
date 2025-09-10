from agents import Agent , Runner , AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled , SQLiteSession
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()

gemini_api_key: str = os.environ.get("GEMINI_API_KEY")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client,
    model='gemini-2.5-flash'
)


set_tracing_disabled(True)

@function_tool
def search(query : str) -> str:
    """ Search """
    return f"You search for {query}"

search_agent: Agent = Agent(
    name='search_agent',
    instructions="You are search agent",
    tools=[search],
    model=model
)


main_agent: Agent = Agent(
    name='main_agent',
    instructions='You are main agent',
    handoffs=[search_agent],
    model=model
)

session = SQLiteSession(session_id='my-session', db_path='test.db')

async def main():
    while True:
        user_input = input("Enter your prompt ")
        if user_input in ['quit' , 'exit' , 'close']:
            break
        runner  = await Runner.run(
            main_agent,
            user_input,
            session=session
        )

        print(runner.final_output)

asyncio.run(main())