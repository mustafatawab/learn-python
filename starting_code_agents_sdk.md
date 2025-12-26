### Boiler Plat Code for the OpenAI Agent SDK with GEMINI

```cmd
pip install -Uq open-agents | pip install -Uq "openai-agents[litellm]"

uv add openai-agents
```


###  Model Configuration
* Global Level
* Run Level
* Agent Level

**Agent Level**
```python
from agents import Agent, Runner, AsyncOpenAI , OpenAIChatCompletionModel, ModelSettings
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.get("GEMINI_API_KEY")

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",

)


model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client,
    model='gemini-2.0-flash'
)


config: RunConfig = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)


run: Runner = Runner.run_sync(
    agent,
    "HI, Can you please solve this (2/2*1000+90) ? ",
)


print(run.funal_output)

```


**Run Level**
```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

gemini_api_key = ""

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print(result.final_output)

```


**Global Level**
```python

from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api

gemini_api_key = ""
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="gemini-2.0-flash")

result = Runner.run_sync(agent, "Hello")

print(result.final_output)
```




