## Learn Python ##


* Agent is an LLM call
* Chat Completion API adopted by almost all companies
* Open AI announce Responsives API which is superset of Chat Completion API
* Tool Calling/Function Calling allows them to interact with external functions or tools to perform specific tasks.
* LLM is stateless. It does not know what was my previous question


### System Prompt
* Give Instruction to the Agent. You have to send again and again with every answer
* Persona 



### User Prompt
* User want from the Agent to generate or do so work

![Open AI Agent SDK](openai_agent_sdk/openai-agent-sdk.png)


## Email Agent Mindmap
![Email Agent Mindmap](email_agent_mindmap.png)


<br>
<br>


Three Main Features of OpenAI Agent SDK
* **Agent Loop** 
* **Python First** 
* **Handoffs**: Delegate task between agents
* **Guardrails**: Input and Output Validation and Check in parallel to your agent
* **Function Tools**
* **Tracing**


We can send LLM **Plain Text** and Which **Tool Cal**
1. User Prompt 
    ```python

        
        await Runner.run(agent , "What is decorator in python")

        Runner.run_sync(agent , "What is decorator in python")

    ```
    **Streaming**
    ```python     
        from openai.types.responses import ResponseTextDeltaEvent
        
        result = Runner.run_streamed(agent , "What is decorator in python")
        async for event in result.stream_events():
            print(event)
            if event.type == 'raw_response_event' and isinstance(event.data, ResponseTextDeltaEvent):
                print(f"\n[DATA] {event.data.delta}") 
     ```
2. System Prompt (Agent Persona = How an agent will behave)
    ```python
    Agent(name='Instructor' , instructions='You are an instructor of python' , model='', tools=[get_weather])
    ```
3. Tool Scheema
    ```python
    from agents import function_tool

    @function_tool
    def get_weather(city: str) -> str:
        return f"Nice weather at {city}"
    ```
4. Final output

By Default the Agent SDK user gpt-4o when you set the OPENAI_API_KEY.

We can connect built-in tools mentioned in the [docs](https://openai.github.io/openai-agents-python/tools/) just with the openai key. 

