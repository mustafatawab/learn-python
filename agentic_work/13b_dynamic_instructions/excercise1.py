from agents import Agent, Runner, RunConfig, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool,RunContextWrapper
from dotenv import load_dotenv
import os
import datetime
load_dotenv()
import asyncio


gemini_api_key = os.environ.get("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Please set gemini api key")

client = AsyncOpenAI(api_key=gemini_api_key , base_url='https://generativelanguage.googleapis.com/v1beta/openai/')

llm_model = OpenAIChatCompletionsModel(openai_client=client, model="gemini-2.0-flash")

def context_aware(wrapper : RunContextWrapper, agent : Agent):
    message_count = len(getattr(wrapper, 'messages', []))
    print(message_count)
    if message_count == 0:
        return "You are a welcoming assistant. Introduce yourself!"
    elif message_count < 3:
        return "You are a helpful assistant. Be encouraging and detailed."
    else:
        return "You are an experienced assistant. Be concise but thorough."

def time_based(wrapper : RunContextWrapper, agent: Agent):
    current_hour = datetime.datetime.now().hour
    print(current_hour)
    if 6 <= current_hour < 12:
        return f"You are {agent.name}. Good morning! Be energetic and positive."
    elif 12 <= current_hour < 17:
        return f"You are {agent.name}. Good afternoon! Be focused and productive."
    else:
        return f"You are {agent.name}. Good evening! Be calm and helpful."


class StatefulInstructions:
    def __init__(self):
        self.interaction_count = 0
        print(self.interaction_count)
    
    def __call__(self, context: RunContextWrapper, agent: Agent) -> str:
        self.interaction_count += 1
        
        if self.interaction_count == 1:
            return "You are a learning assistant. This is our first interaction - be welcoming!"
        elif self.interaction_count <= 3:
            return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation."
        else:
            return f"You are an experienced assistant. We've had {self.interaction_count} interactions - be efficient."

instruction_gen = StatefulInstructions()




async def async_instructions(context: RunContextWrapper, agent: Agent) -> str:
    # Simulate fetching data from database
    await asyncio.sleep(0.1)
    current_time = datetime.datetime.now()
    
    return f"""You are {agent.name}, an AI assistant with real-time capabilities.
    Current time: {current_time.strftime('%H:%M')}
   """


agent = Agent(
    name='General_agent',
    instructions=async_instructions,
    model=llm_model
)

result = Runner.run_sync(
    starting_agent=agent,
    input='hi, what is your name? What is the current time'
)

print(result.final_output)