Install chainlit

``` uv add  chainlit ```

Run Server

``` uv run chainlit run main.py -w ```

Code

```python

import chainlit as cl

@cl.on_message
async def start_chat(message: cl.Message):

    await cl.Message(content=f'Recieved {message.content}').send()

```

```python

import chainlit as cl



```