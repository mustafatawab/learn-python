from agents import Agent , Runner , RunConfig , AsyncOpenAI, OpenAIChatCompletionsModel , function_tool, RunResult, handoff, RunContextWrapper
from dotenv import load_dotenv, find_dotenv
import os
import asyncio
from agents.run import AgentRunner, set_default_agent_runner

from langfuse import get_client
from openinference.instrumentation.openai_agents import OpenAIAgentsInstrumentor

_: bool = load_dotenv(find_dotenv())

# Instrumentation Setup
OpenAIAgentsInstrumentor().instrument()

gemini_api_key: str = os.getenv("GEMINI_API_KEY")
model_name : str = os.getenv("MODEL")
base_url: str = os.getenv("BASE_URL")


# Langfuse Client Initalized 
langfuse = get_client()


if langfuse.auth_check():
    print("\n✅Langfuse client is Authenticated !! ")
else:
    print("❌ Authentication failed. Please check your credentials and host.")



@function_tool(name_override="search_for_file")
async def abc(file_name : str) -> str:
    """ Search file """
    return f"User searching for {file_name}"


external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model=model_name,
    openai_client=external_client
)

runner_config: RunConfig = RunConfig(
    model_provider=external_client,
    model=llm_model,
    tracing_disabled=False
)


class CustomAgentRunner(AgentRunner):
    async def run(self, starting_agent, input, **kwargs):
        print(f"CustomAgentRunner.run()")

        result = await super().run(starting_agent, input, **kwargs)
        return result


        

set_default_agent_runner(CustomAgentRunner())

def onfilesearch(context: RunContextWrapper):
    print("Handoff to filsearch agent")

file_search_agent : Agent = Agent(
    name="file_search",
    instructions="You are only responsible for the file search using your tool",
    tools=[abc]
)

main_agent: Agent = Agent(
    name='personal_assistant',
    instructions="You are helpful personal assistant",
    handoffs=[handoff(file_search_agent , on_handoff=onfilesearch)],
)


async def run() -> None:
    res: RunResult  = await Runner.run(
        starting_agent=main_agent,
        input='Hello,',
        run_config=runner_config
    )

    print(type(res))
    print(res.final_output)


asyncio.run(run())