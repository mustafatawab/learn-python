### Boiler Plat Code for the OpenAI Agent SDK with GEMINI

```cmd
pip install -Uq open-agents | pip install -Uq "openai-agents[litellm]"

uv add openai-agents
```

```python
from agents import Agent, Runner, AsyncOpenAI , OpenAIChatCompletionModel, function_tool , RunConfig, ModelSettings
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


@function_tool
def math_problem(problem: str) -> str:
    """ Solving Math and Programming problems """
    print(f"[TOOL CALLING] {problem}")
    return f"Your Problem is {problem} very complicated"





agent: Agent = Agent(
    name="problem_solver"
    instructions="You are a problem solver"
    model=model
    tools=[math_problem]
)


run: Runner = Runner.run_sync(
    agent,
    "HI, Can you please solve this (2/2*1000+90) ? ",
    config=config
)


print(run.funal_output)

```


