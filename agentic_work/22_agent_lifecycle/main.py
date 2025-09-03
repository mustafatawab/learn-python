from agents import OpenAIChatCompletionsModel, Agent, Runner, function_tool, AgentHooks, RunContextWrapper, Tool, ModelResponse
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import asyncio


load_dotenv()
gemini_api_key: str = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Please Check your GEMINI API key")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client,
    model='gemini-2.5-flash'
)


@function_tool(name_override='get_weather_data' , description_override='Get Weather data for multiple locations')
def get_weather(location: str) -> str:
    return f"the weather in {location} is somehow good."
    


class MyAgentHook(AgentHooks):
    
    def __init__(self, lifecycle):
        super().__init__()
        self.lifecycle = lifecycle
        print("Lifecycle : " , lifecycle)
    
    def on_start(self, context : RunContextWrapper, agent: Agent):
        print("\n --- on_start \n")
        print("\n context " , context.context)
        print("\n agent name " , agent.name)

        return super().on_start(context, agent)

    def on_end(self, context: RunContextWrapper, agent: Agent, output: str):
        print("\n\n on_end \n")
        print("Context" , context)
        print("\n agent name" , agent.name)
        print("\n output " , output)
        return super().on_end(context, agent, output)
    

    def on_handoff(self, context: RunContextWrapper, agent:Agent, source:Agent):
        print("\n\n on_handoff \n")
        print("Context" , context)
        print("\n agent name" , agent.name)
        print("\n source agent name" , source.name)

        return super().on_handoff(context, agent, source)

    def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool : Tool):
        print("\n\n on_tool_start \n")
        print("Context" , context)
        print("\n agent name" , agent.name)
        print('\n Tool ' , tool)
        return super().on_tool_start(context, agent, tool)

    def on_tool_end(self, context: RunContextWrapper, agent: Agent, tool : Tool, result: str):
        print("\n\n on_tool_end \n")
        print("Context" , context)
        print("\n agent name" , agent.name)
        print('\n Tool ' , tool)
        print('\n Result  ' , result)

        return super().on_tool_end(context, agent, tool, result)    


    def on_llm_start(self, context: RunContextWrapper, agent: Agent, system_prompt : str, input_items: list):
        print("\n\n on_llm_start \n")
        print("Context" , context)
        print("\n agent name" , agent.name)
        print('\n System Prompt ' , system_prompt)
        print('\n Input Items ' , input_items)

        return super().on_llm_start(context, agent, system_prompt, input_items)
    
    def on_llm_end(self, context: RunContextWrapper, agent: Agent, response: ModelResponse):
        print("\n\n on_llm_end \n")
        print("Context" , context)
        print("\n agent name" , agent.name)
        print("\n response " , response)


        return super().on_llm_end(context, agent, response)


news_agent: Agent = Agent(
    name='news_agent',
    instructions='You are helpful news agent',
    model=model,
    hooks=MyAgentHook("news_agent_lifecycle")
)


weather_agent : Agent = Agent(
    name='weather agent',
    instructions='You are weather agent',
    model=model,
    tools=[get_weather],
    hooks=MyAgentHook("weather_agent_lifecycle")
)


agent: Agent = Agent(
    name='General Agent',
    instructions="You are general agent",
    model=model,
    handoffs=[news_agent , weather_agent],
    hooks=MyAgentHook("main_agent_lifecycle")
)


async def main():

    runner : Runner = await Runner.run(agent, "what is your name? What is the weather in lahore ")
    print("LLM Result : " ,runner.final_output)


asyncio.run(main())
