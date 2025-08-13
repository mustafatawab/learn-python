from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled, function_tool, RunContextWrapper,ItemHelpers
from dotenv import load_dotenv, find_dotenv
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent

import os
import asyncio
from dataclasses import dataclass
from tavily import AsyncTavilyClient

_: bool = load_dotenv(find_dotenv())

gemini_api_key = os.environ.get("GEMINI_API_KEY")
tavily_key = os.environ.get("TAVILY_KEY")

if not gemini_api_key or not tavily_key:
    raise ValueError("Please set the gemini api key or tavily api key")

tavily = AsyncTavilyClient(api_key=tavily_key)

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

@dataclass
class LocalContext:
    name : str
    tone : str

@function_tool
async def browse(ctx : RunContextWrapper[LocalContext] , query : str) -> str:
    res = await tavily.search(query=query)
    print("Context = " , ctx)
    return f"You searched for this {query} and the result is {res}"


def dynamic_intructions(ctx : RunContextWrapper[LocalContext], agent: Agent):
    return (
        f"You are a {ctx.context.name}"
        f"Your tone is {ctx.context.tone}"
    )


llm_model: OpenAIChatCompletionsModel  = OpenAIChatCompletionsModel(
    openai_client=external_client,
    model='gemini-2.0-flash'
)

run_config: RunConfig = RunConfig(
    model=llm_model,
    model_provider=external_client,
    tracing_disabled=True
)


agent: Agent = Agent(
    name='General Assistant',
    instructions=dynamic_intructions,
    tools=[browse]
)


async def main():
    context = LocalContext(name='travel agent' , tone='friendly')
    result: Runner =  Runner.run_streamed(
        agent ,
        "Hi, How are you. Search about FastAPI and lemme know what can i build on it",
        run_config=run_config,
        context=context
    )

    async for event in result.stream_events():
        # if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        #     print(event.data.delta, end="", flush=True)
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types





asyncio.run(main())