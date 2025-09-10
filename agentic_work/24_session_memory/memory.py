from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled, SQLiteSession
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

gemini_api_key: str = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model='gemini-2.5-flash'
)

set_tracing_disabled(True)

@function_tool
def search(query: str) -> str:
    """ Search """
    return f"You search for {query}"


session: SQLiteSession = SQLiteSession(session_id='general-session', db_path='general_test.db')

agent: Agent = Agent(
    name='general_agent',
    instructions="You are a general agent",
    tools=[search],
    model=llm_model,
)



async def session_operation():
    
    await session.clear_session()
    print("\n\n Session " , session.get_items())



    await session.add_items([
        {"role": "user", "content": "what is my name"},
        {"role": "assistant", "content": "your name is John"},
        {"role": "user", "content": "what is my age"},
        {"role": "assistant", "content": "your age is 30"},
    ])

    items = await session.get_items()

    print("\n\n Session Items : \n" , items)

    last_item = await session.pop_item()
    print("\n Last Item removed : " , last_item)

   



asyncio.run(session_operation())
# async def main():

#     result: Runner = await Runner.run(
#         agent,
#         "what is my name",
#         session=session

#     )

#     print(result.final_output)


# asyncio.run(main())