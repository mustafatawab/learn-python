from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled, SQLiteSession, RunContextWrapper
from agents.tool_context import ToolContext
from dotenv import load_dotenv
from dataclasses import dataclass
import asyncio
from mem0 import MemoryClient
import os


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
mem0_api_key = os.getenv("MEM0_API_KEY")

if not gemini_api_key or not mem0_api_key:
    raise ValueError("GEMINI_API_KEY and MEM0_API_KEY must be set in environment variables")


mem0_client = MemoryClient()

set_tracing_disabled(True)

client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.5-flash",
)

@dataclass
class UserContext:
    username : str


@function_tool
async def search_user_memory(context: ToolContext[UserContext], query: str):
    """ Use this tool to search the user memory """
    print("\n\n Searching memory for:", query)
    print("\n\n context in search user memory :", context)
    reponse =  mem0_client.search(query=query , user_id=context.context.username)
    return reponse

@function_tool
async def save_user_memory(context: ToolContext[UserContext], query: str) -> str:
    """ Use this tool to save the user memory """
    print("\n\n Saving to memory:", query)
    print("\n\n context in saving memory :", context)
    response =  mem0_client.add([{"role" : "user", "content": query}], user_id=context.context.username)
    return response

@function_tool
async def get_user_memories(context: ToolContext[UserContext]):
    """ Use this tool to get all user memories """
    print("\n\n Getting all memories for user:", context.context.username)
    response =  mem0_client.get_all(user_id='1001')
    print("\n\n Getting all memories " , response)
    return response

    



def dynamic_instructions(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:

    # past_memories = mem0_client.search(query="General Behavior" , user_id=context.context.username , top_k=3)
    past_memories = mem0_client.get_all(user_id=context.context.username)
    return f"""
        You are a helpful assistant. Here are some of the user's past memories that might help you:
        {past_memories}. Use tools to find and add memories as needed.

     """

agent : Agent = Agent(
    name="agent",
    instructions=dynamic_instructions,
    model=model,
    tools=[search_user_memory , get_user_memories , save_user_memory]
)

async def main() -> None:

    context: UserContext = UserContext(username="1001")

    while True:
        user_input = input("Enter your prompt: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Exiting...")
            break   
        result : Runner = await Runner.run(agent , user_input , context=context)

        print("\n\n LLM Response" , result.final_output)


asyncio.run(main())