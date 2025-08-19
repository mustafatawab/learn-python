from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunContextWrapper
from dotenv import load_dotenv
import os
import asyncio
from dataclasses import dataclass, field

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

@dataclass
class Products:
    products: list[str] = field(default_factory=lambda:["Watch", "Phone", "Laptop", "Tablet" , "Headphones" , "Charger " , "Camera" , "Speaker" , "Monitor" , "Keyboard"])



@function_tool
async def get_order_status(wrapper: RunContextWrapper[Products] , order_id: str) -> str:
    """ Get the status of an order by its ID."""
    return f"Order {order_id} is currently being processed."

order_tracking_agent: Agent = Agent(
    name="Order Tracking Agent",
    instructions="You are an order tracking assistant. You can help users track their orders.",
    model=model,
    tools=[get_order_status]
)

product_inquiry_agent: Agent = Agent(
    name="Product Inquiry Agent",
    instructions="Answer questions about products details , specifications  and their availability.",
    model=model
)

support_agent: Agent = Agent(
    name="Support Agent",
    instructions="You are a support agent. You can assist users with general inquiries.",
    model=model,
)


def agent_instructions(wrapper: RunContextWrapper[Products] , agent: Agent) -> str:
    """Provide instructions for the main agent."""
    print(f"Context products: {wsrapper.context.products}")
    return (
        f"All prouducts are {wrapper.context.products}. "
        f"You can assist users with general inquiries. "
        f"Your name is {agent.name}. "

    )


all_products = ["Watch", "Phone", "Laptop", "Tablet" , "Headphones" , "Charger " , "Camera" , "Speaker" , "Monitor" , "Keyboard"]
product = Products(products=all_products)

async def main()->None:

    main_agent: Agent = Agent(
        name="Main Agent",
        instructions=agent_instructions,
        model=model,
        handoffs=[handoff(support_agent) , handoff(order_tracking_agent) , handoff(product_inquiry_agent)],
    )

    result : Runner = await Runner.run(
        main_agent,
        input("Enter your prompt about order tracking, product inquiries, or support: "),
        context=product
    )

    print(result.final_output)


asyncio.run(main())
