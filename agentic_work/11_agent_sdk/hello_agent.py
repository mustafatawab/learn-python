from agents import Agent , Runner , AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
import asyncio
import nest_asyncio

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key:
    raise ValueError("Please set gemini api key")


external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=external_client
)

agent: Agent = Agent(
    name='General Assistant',
    instructions='You are general assistant. But You can search also from the internet.',
    model=model,
)


def RunnAgentSync()->None:
    content: str = input("How Can I help you ? ")
    runner : Runner = Runner.run_sync(
        agent , 
        content,
    )
    print("------Calling Agent - Synchronously--------- \n")
    print(runner.final_output)
    print("-------END of Agent------------")

async def RunnAgentAsync() -> None:
    content: str = input("How can I help you? ")
    runner: Runner = await Runner.run(
        agent,
        content
    )
    print("------Calling Agent - Asynchronously--------- \n")
    print(runner.final_output)
    print("-------END of Agent------------")

if __name__ == "__main__":
    usr : str = input("what would you like Syncrounse or Asyncrounouse?  Write (sync) or (async) ").lower()
    if usr == 'async':
        asyncio.run(RunnAgentAsync())
    elif usr == 'sync':
        RunnAgentSync()
    else:
        raise ValueError("Please Choose the right option....")
