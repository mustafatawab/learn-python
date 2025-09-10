from agents import Agent , Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool, handoff, RunHooks, RunContextWrapper, ModelResponse,Tool, RunResult

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

user_chat: list[dict] = []
while True:
    user_input = input("Enter you prompt (exit or quit)")
    if user_input in ['exit' , 'quit']:
        break

    user_message = {"role" : "user" , "content" : user_input}
    user_chat.append(user_message)

    res: RunResult = Runner.run_sync(main_agent , user_chat , run_config=config)

    user_chat = res.to_input_list()
    print(res.final_output)