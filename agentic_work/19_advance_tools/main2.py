from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, AgentBase, function_tool, RunContextWrapper, set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import asyncio
import os
from pydantic import BaseModel
from dataclasses import dataclass
from agents.run import RunConfig


load_dotenv()


gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
) 

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.0-flash",
)

# @dataclass
class UserContext(BaseModel):
    user_id : str
    permission: bool
    subscription: str = "free"


async def has_permision(ctx: RunContextWrapper[UserContext] , agent: AgentBase[UserContext]) -> bool:
    print("Has permission check called\n")
    print(ctx.context.subscription, ctx.context.subscription in ['pro' , 'premium' , "enterprise"])
    return ctx.context.subscription in ['pro' , 'premium' , "enterprise"]

@function_tool(is_enabled=has_permision)
def get_user_info() -> str:
    """ Get user information """
    return "User information retrieved successfully."

run_config = RunConfig(
    model=llm_model,
    model_provider=client,
    tracing_disabled=True
)

agent: Agent = Agent(
    name='General Agent',
    instructions='You are a general agent. You will write creative but short.',
    tools=[get_user_info],
)

user_context:UserContext = UserContext(
    user_id="12345",
    permission=True,
    subscription="free" 
)

result : Runner = Runner.run_sync(
    starting_agent=agent,
    input='Hi, Please retreive the information of the users',
    run_config=run_config,
    context=user_context
)

print(result.final_output)
