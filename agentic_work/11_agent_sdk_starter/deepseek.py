from agents import Agent , Runner , AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
import asyncio
import nest_asyncio

load_dotenv()

deepseek_key = os.getenv("DEEPSEEK_API_KEY")


if not deepseek_key:
    raise ValueError("Please set deekseek api key")




external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=deepseek_key,
    base_url="https://api.deepseek.com/v1"
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="deepseek-chat",
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
