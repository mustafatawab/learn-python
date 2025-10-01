(Agentic AI Presentation)[https://docs.google.com/presentation/d/1VNFGsCYMDT1VTe8W1wxFbmAwYsJ1I0Y-6CnTvuCEn98/edit?slide=id.g349e80b1802_4_87#slide=id.g349e80b1802_4_87]


# **Artificial Intelligence**

Three waves of AI
1. Predictive AI
    * Predict based upon the data
    * Analyze past data to predict future outcomes
    * example : Is this is cat or not?
2. Generative AI
    * Generating Content (Text , Images, Code , Video)
    * Content Creator
    * example: Can generate text about cat
3. Agentic AI
    * A bot on your behaf.
    * Autonomous actions and learning iteratively.
    * Automate repetative Task.
    * It's like artificial human. 
    * You use LLM to create your intelligent Apps.



## AI Agent 
    1. Software Agents
    2. Physical Agents - e.g Robots , Automated Vehicles etc


**DACA**
    1. AI First
    2. Cloud First
    3. Develop Anywhere
    4. Cloud/Deploy Anywheres



**OpenAI Chat Completion's API** ***(Stateless)***
    * Standardized and adapted by the world wide
    * You can use any LLM with OpenAI Chat Comletions API. In this case we use gemini.

```python
from openai import OpenAI

client = OpenAI(api_key=your_api_key, base_url='https://generativelanguage.googleapis.com/v1beta/openai/')


response = client.chat.completions.create(
    model='gemini-2.5-flash',
    messages=[
        {"role" : "system" , "content" : "You are helpful assistant"},
        {"role" : "user" , "content" : "Your content goes here."},
    ]
)


result = response.choices[0].message.content
print(result)

```

**OpenAI Responses API** ***(Stateful, tool-ready)***
    * server store user history
    * Bult-in tools
        * Web Search
        * File Retrieval
        * Code interpreter
        * Image Generation
    * OpenAI Agent SDK use built in reponses api but you can use chat completions api too if you want




____

-----------



# OpenAI Agents SDK


##  Model Configuration
* Global Level
* Run Level
* Agent Level

**Agent Level**
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


## Tool Calling
External tool that the agent will call.
```python

from agents import function_tool, Agent

@function_tool
def search(query: str) -> str:
    """ Search the browser """
    return query

agent = Agent(
    name='..',
    instructions='....',
    tools=[search]
)
```


## Model Settings
LLM Settings like temperature, max_tokens, top_p

```python

from agents import function_tool, Agent, ModelSettings

agent = Agent(
    name='..',
    instructions='....',
    model_settings=ModelSettings(
        temperature=0.8,
        top_p=0.9,
        parallel_tool_use=False,
        max_tokens=1000,
        tool_choice='auto'. # required, auto, none
    )
)
```

## Local Context
Additional Information for the Agent to dynamically decide what to do.
```python
from agents import RunContextWrapper
from dataclasses import dataclass


@dataclass
class TravelContext:
    name: str
    tone: str 
    destination: str

travel_context = TravelContext(name='....' , tone='helpful' , destination='hunza')

result = Runner.run_sync(
    context=travel_context
)

```


## Dynamic Instructions
Dynamically instructions for the agent and it will take a Callable

```python
from agents import RunContextWrapper, Agent

def my_agent_instructions(wrapper: RunContextWrapper[TravelContext] , agent: Agent[TravelContext]) -> str:
    return f""" You are {agent.name}. Be Helpful and Friendly. The destination is {wrapper.context.destination} with {wrapper.context.tone} tone """

agent = Agent(
    name='travel_guide',
    instructions=my_agent_instructions
)
```


## Runner
Runner is the engine of the agent that will run it and use LLM as a brain.
1. Synchronous
2. Asynchronous
3. Streaming


```python
from agent import Runner
result = Runner.run_sync(agent,"user prompt goes here")

```


```python
from agent import Runner

async def main():
    result = await Runner.run(agent,"user prompt goes here")

```


**Streaming**
```python
from agent import Runner

async def main():
    result = Runner.run_streamed(agent,"user prompt goes here")
     if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        print(event.data.delta , end='')
```
```python
from agent import Runner

async def main():
    result = Runner.run_streamed(agent,"user prompt goes here")
     if event.type == 'run_item_stream_event':
            if event.item.type == "message_output_item":
                print(ItemHelpers.text_message_output(event.item))
```


## Agent Cloning



## Tracing


## Agent as Tool


## Handoff