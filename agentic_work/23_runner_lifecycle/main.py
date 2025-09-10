from agents import Agent , Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunHooks, RunContextWrapper, ModelResponse,Tool

from dotenv import load_dotenv
import os

load_dotenv()

gemini_api_key: str = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("Please set the gemini api key")

client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=client,
    model='gemini-2.5-flash'
)



config: RunConfig = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)


class MyRunnerHook(RunHooks):
    
    def on_agent_start(self, context:RunContextWrapper, agent: Agent):
        print('ON agent start' , context , agent)
        
        return super().on_agent_start(context, agent)

    def on_agent_end(self, context: RunContextWrapper, agent: Agent, output):
        print("On agent end" , context , agent , output)
        return super().on_agent_end(context, agent, output)
    
    def on_llm_start(self, context:RunContextWrapper, agent:Agent, system_prompt:str, input_items:list):
        print("on llm start")
        return super().on_llm_start(context, agent, system_prompt, input_items)

    def on_llm_end(self, context: RunContextWrapper, agent:Agent, response: ModelResponse):
        print("on llm end")
        return super().on_llm_end(context, agent, response)

    def on_handoff(self, context :RunContextWrapper, from_agent: Agent, to_agent:Agent):
        print("on handoff")
        return super().on_handoff(context, from_agent, to_agent)
    
    def on_tool_start(self, context:RunContextWrapper, agent:Agent, tool : Tool):
        print("on tool start")
        return super().on_tool_start(context, agent, tool)
    
    def on_tool_end(self, context:RunContextWrapper, agent:Agent, tool:Tool, result:str):
        print("ON tool end")
        return super().on_tool_end(context, agent, tool, result)
    


    
@function_tool(description_override='Weather information about specific location')
def weather_info(city: str) -> str:
    return f"The weather is very good at {city}"

weather_agent : Agent = Agent(
    name='weather_agent',
    instructions='Get information about the weather. You have tool to use for the weather information',
    tools=[weather_info]
)


planning_agent: Agent = Agent(
    name='planing_agent',
    instructions='Plan the user query by dividing into the sub parts. It means breaking down the whole query is the main task.'    
)

main_agent: Agent = Agent(
    name='main_agent',
    instructions='You are main agent and a general assistant too',
    handoffs=[handoff(planning_agent) , handoff(weather_agent)]
)

result : Runner = Runner.run_sync(
    starting_agent=main_agent,
    input="Hi, What is the weather in swat",
    run_config=config,
    hooks=MyRunnerHook()
)


print(result.final_output)

