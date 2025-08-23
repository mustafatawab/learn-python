from agents import Agent , Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper, handoff
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

gemini_api_key: str = os.environ.get('GEMINI_API_KEY')
if not gemini_api_key:
    raise ValueError("Please set the GEMINI api key")

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    ),

    model='gemini-2.0-flash'
)

@function_tool
def get_weather(location: str) -> str:
    """ Get Weather """
    print("Weather tool called")
    return f"The weather in {location} is awesome"

def is_news_agent_allowed(wrapper : RunContextWrapper , agent : Agent) -> bool:
    return True

weather_agent: Agent = Agent(
    name='weather_agent',
    instructions='you are weather agent',
    tools=[get_weather]
)

news_agent: Agent = Agent(
    name='news_agent',
    instructions='You are news agent. You will get latest news about tech industry',
    handoffs=[handoff(weather_agent)]
)

weather_agent.handoffs = [news_agent]



agent: Agent = Agent(
    name='general_agent',
    instructions='You are general assistant. You can transfer the user query to the other agents.',
    model=model,
    handoffs=[handoff(
        agent=news_agent,
        is_enabled=is_news_agent_allowed
    )]
)



async def streaming():
    result: Runner =  Runner.run_streamed(
        agent,
        "Hey, What GPT-5 can do?"
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
            print(event.data.delta , end="", flush=True)


async def main() -> None:
    result: Runner = await Runner.run(
        agent, 
        "Hi"
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())