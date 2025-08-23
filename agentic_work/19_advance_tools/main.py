from agents import AgentBase, AsyncOpenAI, OpenAIChatCompletionsModel , Agent, Runner, function_tool, RunContextWrapper, ItemHelpers
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv
import asyncio
import os
from agents.run import RunConfig
from dataclasses import dataclass
from pydantic import BaseModel
# Load environment variables from .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash",
)

@dataclass
class UserScope(BaseModel):
    is_admin: bool


@function_tool(is_enabled=False, name_override="maintainence_work" , description_override="Check the tool if it is under maintainence or not")
def under_maintainence():
    """ This tool is temporarily disabled """
    return "Sorry, This feature is offline for maintainence"



def allow_db_deletion(wrapper: RunContextWrapper[UserScope], agent: AgentBase[UserScope]) -> bool:
    return True if wrapper.context.is_admin else False

@function_tool()
def delete_user_db(is_enabled=allow_db_deletion):
    """ Delete the entire user database """
    return "User database deleted successfully."




config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

agent = Agent(
    name='my_agent',
    instructions='You are my main agent. You will write creative but short.',
    tools=[under_maintainence, delete_user_db],

)


async def main()->None:
    admin: UserScope = UserScope(is_admin=False)


    result =  Runner.run_streamed(
        agent,
        "HI, How is going your day. Please the user database",
        run_config=config,
        context=admin
    )

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end='', flush=True)



asyncio.run(main())