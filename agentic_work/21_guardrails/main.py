from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool,RunContextWrapper, GuardrailFunctionOutput, input_guardrail, output_guardrail, InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered, TResponseInputItem
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from pydantic import BaseModel


load_dotenv()

gemini_api_key: str = os.environ.get("GEMINI_API_KEY")

openai_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

gemini_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    openai_client=openai_client,
    model='gemini-2.0-flash'
)



class WeatherData(BaseModel):
    weather_related : bool
    reason: str

weather_sanatizer: Agent = Agent(
    name='weather_checker',
    instructions='you will check weather it is weather related or not',
    output_type=WeatherData,
    model=gemini_model
)

@function_tool
def get_weather(location: str) -> str:
    """ Get Weather of the city """
    return f"The weather in {location} is sunny"

@input_guardrail
async def check_weather_input(wrapper : RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    print("\n[Context]" , wrapper.context)
    print("\n[agent name]" , agent.name)
    print("\n[input]" , input)
    result =await Runner.run(weather_sanatizer , input , context=wrapper.context)

    return GuardrailFunctionOutput(
        output_info='weather passed',
        tripwire_triggered=result.final_output.weather_related is False
    )


@output_guardrail
def check_weather_output(wrapper: RunContextWrapper[None], agent: Agent, input : str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    print("\n-------")
    print("\n[context]" , wrapper.context)
    print("\n[agent name]" , agent.name)
    print("\n [input]" , input)
    return GuardrailFunctionOutput(
        output_info='output passed',
        tripwire_triggered=False
    )



weather_agent: Agent = Agent(
    name="weather_agent",
    instructions='You are weather agent you will respond about the weather only.',
    model=gemini_model,
    tools=[get_weather],
    input_guardrails=[check_weather_input],
    output_guardrails=[check_weather_output]
)

try:
    result: Runner = Runner.run_sync(
        weather_agent,
        "What is best place in swat"
    )

    print(result.final_output)
except InputGuardrailTripwireTriggered as e:
    print("-- Input Guardrail Tripwire Triggered -- ")
except OutputGuardrailTripwireTriggered as e:
    print("-- Output Guardrail triggered -- ")
