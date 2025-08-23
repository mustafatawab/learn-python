import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, HandoffInputData
import asyncio
from agents.extensions import handoff_filters
from agents.extensions.handoff_filter import RECOMMENDED_PROMPT_PREFIX
_: bool = load_dotenv()

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
if not gemini_api_key:
    raise ValueError("Please set the gemini api key")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)


@function_tool
def get_weather(city: str) -> str:
    print("\n Weather tool called \n")
    return f"The weather in {city} is rainy"


def summarized_news_transfer(data: HandoffInputData) -> HandoffInputData:
    print("Summaraized News Transfer " , data)
    summarized_conversation='get latest tech news'
    return HandoffInputData(
            input_history=summarized_conversation,
            pre_handoff_news=(),
            new_items=()
    )

news_agent: Agent = Agent(
    name='news_agent',
    instructions='Get latest news on what the user ask but it must be about technology. You will handoff to the weather_agent',
    model=llm_model,

)

weather_agent: Agent = Agent(
    name='weather_agent',
    instructions='You only respond to the user about the weather. Also you will handoff to the news_agent ',
    tools=[get_weather],
    model=llm_model,
    handoffs=[handoff(
        agent=news_agent,
        input_filter=summarized_news_transfer
    )]
)

news_agent.handoffs=[handoff(weather_agent)]

def dynamic_instructions(ctx , agent):
    return (
        f"{RECOMMENDED_PROMPT_PREFIX}",
        "You will listen to the user query and transfer to other agents"
    )

main_agent: Agent = Agent(
    name='orchestrator_agent',
    instructions=dynamic_instructions,
    model=llm_model,
    handoffs=[handoff(
        agent=weather_agent,
        tool_name_override='Weather Agent',
        tool_description_override='You are weather agent and will only respond about the weather.',
    ),
    handoff(
        agent=news_agent,
        # input_filter=summarized_news_transfer
        input_filter=handoff_filters.remove_all_tools

    )
    ]
)


async def main()-> None:
    res: Runner = await Runner.run(
        main_agent,
        # "check if any latest news about ChatGPT OPENAI new model which is gpt-5"
        "hi. what is the latest news about the OpenAI New Model. Lemme know weather in United States"
    )

    print(res.last_agent.name)
    print(res.final_output)


asyncio.run(main())