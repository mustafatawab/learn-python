from agents import Agent, Runner, AsyncOpenAI , OpenAIChatCompletionsModel, function_tool, set_tracing_disabled, set_default_openai_client , set_default_openai_api
from dotenv import load_dotenv , find_dotenv
import os
from tavily import TavilyClient
_: bool = load_dotenv(find_dotenv())

gemini_api_key = os.environ.get("GEMINI_API_KEY")
tavily_api_key = os.environ.get("TAVILY_API_KEY")

if not gemini_api_key or not tavily_api_key:
    raise ValueError("Please set Gemini or Tavily api key")

tavily_client = TavilyClient(api_key=tavily_api_key)

set_tracing_disabled(True)
set_default_openai_api("chat_completions")

@function_tool
def search(query: str) -> str:
    """ Perform a Web search  """
    response = tavily_client.search(query=query)
    return str(response)


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="gemini-2.0-flash" , tools=[search])

result = Runner.run_sync(agent, "Hello, Can you search over internet? if yes please find the motivational speaker in Pakistan. You can search Youtube or google")

print(result.final_output)