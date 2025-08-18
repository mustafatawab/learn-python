from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")

if not gemini_key:
    raise ValueError("Please set GEMINI_API_KEY")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_key,
     base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash-exp",
    openai_client=client
)

billing_agent: Agent = Agent(
    name="Billing Agent",
    instructions="You are a billing assistant. You can help users with billing inquiries.",
    model=model
)

refund_agent: Agent = Agent(
    name="Refund Agent",
    instructions="You are a refund assistant. You can help users with refund inquiries.",
    model=model
)

async def main()->None:

    main_agent: Agent = Agent(
        name="Main Agent",
        instructions="You are the main agent. You can assist users with general inquiries. You will listen to the billing and refund agents.",
        model=model,
        handoffs=[billing_agent, refund_agent]
    )

    result : Runner = await Runner.run(
        main_agent,
        "I need billing unit price information in pakistan for the commercial sector."
    )

    print(result.final_output)


asyncio.run(main())
