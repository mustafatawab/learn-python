from agents import Agent, Runner, function_tool, set_tracing_disabled
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Prompt(BaseModel):
    prompt: str

app = FastAPI() 

set_tracing_disabled(True)  # Disable tracing for this run

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL")

# print(MODEL)
if not GEMINI_API_KEY or not MODEL:
    raise ValueError("GEMINI_API_KEY and MODEL must be set in the environment variables.")



agent: Agent = Agent(
    name="Assistant",
    instructions="You only respond in English and Urdu.",
    model=LitellmModel(model=MODEL, api_key=GEMINI_API_KEY),
)

@app.post("/run")
def run_agent(prompt: Prompt):
    result = Runner.run_sync(agent, prompt.prompt.strip())
    print(f"Response: {result.final_output}")
    return {"response": result.final_output}
