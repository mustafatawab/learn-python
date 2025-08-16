from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, RunContextWrapper
from dotenv import load_dotenv
from tavily import TavilyClient
import os
from dataclasses import dataclass
from datetime import datetime

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")


external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)


llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model="gemini-2.0-flash"
)

@function_tool
async def tavily_search(query: str) -> str:
    """ Search the web using Tavily API. """
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY environment variable is not set.")
    client = TavilyClient(api_key=tavily_api_key)
    result = client.search(query=query)
    return result


deep_research_agent : Agent = Agent(
    name='deep_research',
    model=llm_model,
    instructions="You are a deep research agent that can answer questions and help with tasks.",
    tools=[tavily_search]
)

scientis_agent: Agent = Agent(
    name='scientist',
    model=llm_model,
    instructions="You are a scientist that can answer questions and help with tasks.",
)

plaining_agent: Agent = Agent(
    name='plaining',
    model=llm_model,
    instructions="You are a planning agent that can answer questions and help with tasks.",
)

@dataclass
class Instructions:
    instruction : str

def dynamic_instructions(wrapper: RunContextWrapper[Instructions] , agent:Agent) -> str:
    current_date = datetime.now().isoformat()
    return (
        f"You are a {agent.name} agent. "
        f"You will deeply understand the user's request and provide detailed responses"
        f"You are Main agent that will plan , research and reflect the user's request. "
        f"you return the current date when user asks for it. The current date is {current_date}"
    )

agent: Agent = Agent(
    name="agent",
    model=llm_model,
    instructions=dynamic_instructions,
    tools=[scientis_agent.as_tool(
        tool_name="scientist_tool",
        tool_description="A tool that can answer questions and help with tasks.",
    ),
    deep_research_agent.as_tool(
        tool_name="deep_research_tool",
        tool_description="A tool that can perform deep research and answer questions.",
    ),
    plaining_agent.as_tool(
        tool_name="planning_tool",
        tool_description="A tool that can help with planning and organizing tasks.",
    )
    ]
)

context = Instructions(instruction="You are a main agent that will plan, research, and reflect the user's request.")

result: Runner = Runner.run_sync(
    agent,
    input('What is your request? '),
    context=context
)

print(result.final_output)