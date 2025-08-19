from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunContextWrapper,ItemHelpers
from dotenv import load_dotenv
import os
import asyncio
from dataclasses import dataclass, field
from openai.types.responses import ResponseTextDeltaEvent



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

@function_tool
def all_products(wrapper: RunContextWrapper[Products]) -> list[str]:
    """Return all available products."""
    return wrapper.context.products

def product_agent_instructions(wrapper: RunContextWrapper[Products], agent: Agent) -> str:
    "You have all products details and data about the products"
    return (
        f"All Products details are {wrapper.context.products}. "
    )

product_agent: Agent = Agent(
    name="Product Agent",
    instructions=product_agent_instructions,
    model=model,
    tools=[all_products]
)

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


@function_tool
def get_weather(wrapper: RunContextWrapper[Products], location: str) -> str:
    """ Get the weather for a given location."""
    return f"The weather in {location} is sunny with a high of 25°C."


product = Products()

async def main()->None:

    main_agent: Agent = Agent(
        name="Main Agent",
        instructions="You are main agent and will listen to the user queries and handoff to the appropriate agent.",
        model=model,
        tools=[get_weather],
        handoffs=[handoff(support_agent) , handoff(order_tracking_agent) , handoff(product_inquiry_agent), product_agent],
    )

    result : Runner =  Runner.run_streamed(
        main_agent,
        input("Enter your prompt about order tracking, product inquiries, or support: "),
        # context=product
    )

    async for event in result.stream_events():
        # if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
        #     print(event.data.delta , end='' , flush=True)
        # print("\n\n\n" , event.type , "\n\n\n")
        if event.type == "raw_response_event":
            print("Raw Response event ")
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"\nAgent updated: {event.new_agent.name}")
            continue
        elif event.type  == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("\n Tool was called")
            elif event.item.type == "tool_call_output_item":
                print("\n -- Tool output " , event.item.output)
            elif event.item.type == "message_output_item":
                print("\n -- Message Output: " , ItemHelpers.text_message_output(event.item))


asyncio.run(main())
