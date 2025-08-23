from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunContextWrapper
from dotenv import load_dotenv
import os
import asyncio
from dataclasses import dataclass, field
from pydantic import BaseModel

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

@function_tool(is_enabled=True, name_override="all_products" , description_override='Get all available products')
async def get_product_details(wrapper: RunContextWrapper[Products] , product_name: str) -> str:
    """ Get details about a specific product."""
    if product_name in wrapper.context.products:
        return f"Details for {product_name}: This is a great product."
    else:
        return f"Product {product_name} not found."

order_tracking_agent: Agent = Agent(
    name="Order Tracking Agent",
    instructions="You are an order tracking assistant. You can help users track their orders.",
    model=model,
    tools=[get_order_status]
)

product_inquiry_agent: Agent = Agent(
    name="Product Inquiry Agent",
    instructions="Answer questions about products details , specifications  and their availability.",
    model=model,
    tools=[get_product_details]
)

support_agent: Agent = Agent(
    name="Support Agent",
    instructions="You are a support agent. You can assist users with general questions about products and ecommerce.",
    model=model,
)



def agent_instructions(wrapper: RunContextWrapper[Products] , agent: Agent) -> str:
    """Provide instructions for the main agent."""
    print(f"Context products: {wrapper.context.products}")
    return (
        f"All prouducts are {wrapper.context.products}. "
        f"You can assist users with general inquiries. "
        f"Your name is {agent.name}. "
)


class EscilationData(BaseModel):
    reason: str
    topic: str

product = Products()

def handoff_event(ctx: RunContextWrapper[Products] , input_data: EscilationData) -> str:
    print("\n On Handoff event: Context = " , ctx.context.products)
    print(f"\n Escilation  {input_data}")


async def main()->None:

    main_agent: Agent = Agent(
        name="Main Agent",
        instructions=agent_instructions,
        model=model,
        handoffs=[
            handoff(
                agent=support_agent,
                tool_name_override="product_support_agent",
                tool_description_override="Assist with general products, eccomerce and support issues.",
                on_handoff=handoff_event,
                input_type=EscilationData
            ), 
            handoff(
                agent=order_tracking_agent,
                tool_name_override="order_tracking_agent",
                tool_description_override="Assist with order tracking issues.",
                on_handoff=handoff_event,
                input_type=EscilationData
            ), 
            handoff(
                agent=product_inquiry_agent,
                tool_name_override="product_details_agent",
                tool_description_override="Assist with product inquiries and details.",
                on_handoff=handoff_event,
                input_type=EscilationData
            )
        ],
    )

    result : Runner = await Runner.run(
        main_agent,
        input("Enter your prompt about order tracking, product inquiries, or support: "),
        context=product
    )

    print("\n\n LLM Response " , result.final_output)
    print("\nLast Agent Name " ,result.last_agent.name)


asyncio.run(main())
