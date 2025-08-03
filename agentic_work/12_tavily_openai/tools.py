from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool , set_tracing_disabled, set_default_openai_api, set_default_openai_client
from dotenv import load_dotenv, find_dotenv
import os

_: bool = load_dotenv(find_dotenv())
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

@function_tool()
def calculator(a: float, b: float, operation: str) -> float:
    """ Perform a basic arithmetic operation on two numbers."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b
    else:
        raise ValueError("Invalid operation")

@function_tool()
def capital(country: str) -> str:
    """ Return the capital of a given country."""
    capitals = {
        "USA": "Washington, D.C.",
        "France": "Paris",
        "Germany": "Berlin",
        "Japan": "Tokyo",
        "India": "New Delhi",
    }
    return capitals.get(country , "No data available for this country")

agent: Agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model="gemini-2.0-flash",
    tools=[calculator, capital],
)

result: Runner = Runner.run_sync(agent, input("How can I help you ? "))
print(result.final_output)