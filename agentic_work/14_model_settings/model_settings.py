from agents import Agent , Runner , ModelSettings, OpenAIChatCompletionsModel  , function_tool, AsyncOpenAI , set_tracing_disabled
from agents.run import RunConfig

from dotenv import load_dotenv, find_dotenv
import os

_: bool = load_dotenv(find_dotenv())

set_tracing_disabled(True)

gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Please set gemini api key")


client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(openai_client=client, model='gemini-2.0-flash')


agent: Agent = Agent(
    name='my-agent',
    instructions='you are helpful assistant',
    model_settings=ModelSettings(temperature=0.7, tool_choice='auto'),
)


run_config: RunConfig = RunConfig(
    model=model,
    model_provider=client
)

result: Runner = Runner.run_sync(agent, "what is 100 + 90", run_config=run_config)
print(result.final_output)
