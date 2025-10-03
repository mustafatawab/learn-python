from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel,Runner, function_tool, set_tracing_disabled, SQLiteSession, RunContextWrapper
from openai.types.responses import ResponseTextDeltaEvent
import chainlit as cl
from dotenv import load_dotenv
import os
from dataclasses import dataclass

set_tracing_disabled(True)


load_dotenv()
gemini_api_key: str = os.environ.get("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Please Set the gemini api key")

client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

model = OpenAIChatCompletionsModel(
    model='gemini-2.5-flash',
    openai_client=client
)

@dataclass
class MyContext:
    user_id : str
    seen_messages = []
    


@function_tool(name_override="web_search", description_override="Use this tool for searching" , is_enabled=True)
@cl.step(type="web_search")
async def search(wrapper : RunContextWrapper[MyContext] ,query: str) -> str:
      return f"User searching for {query}"



@function_tool(name_override="get_weather" , description_override="Use this tool for weather information")
async def weather_info(wrapper: RunContextWrapper[MyContext] ,city: str) -> str:
      return f"THe weather in {city} is too cold right now"


@function_tool
@cl.step(type="greeting tool")
def greet_user(context: RunContextWrapper[MyContext], greeting: str) -> str:
    user_id = context.context.user_id
    return f"Hello {user_id}, you said: {greeting}"


@cl.set_starters
async def set_starters() -> list[cl.Starter]:
      return [
            cl.Starter(
                  label="swat weather",
                  message="What is the weather in swat"
            ),

            cl.Starter(
                  label="search about Agentic AI",
                  message="Search about agentic AI"
            ),

            cl.Starter(
                  label="karachi weather",
                  message="what is the weather in karachi"
            ),

            cl.Starter(
                  label="Search AI Tools",
                   message="Search about latest AI tools"      
            )
      ]


agent = Agent(
    name='helpful_assistant',
    instructions="You are helful assistant. You are responsisble to respond friendly.Call greet_user tool to greet the user. Always greet the user when session starts. ",
    model=model,
    tools=[search, weather_info, greet_user]
)

user_history  = {}

@cl.on_message
async def conversation(message: cl.Message):
        msg = cl.Message(content="Thinking....")
        await msg.send()

        my_ctx = MyContext(user_id="Zia")

        user_id = "p002"
        if user_id not in user_history:
              user_history[user_id] = SQLiteSession("conversation_001" , "converstation_db")
        
        session = user_history[user_id]

        
        result =  Runner.run_sync(agent , message.content, session=session, context=my_ctx)

        msg.content = result.final_output

        await msg.send()
        

        