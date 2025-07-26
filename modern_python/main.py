import asyncio

async def myfunction():
    print("Hello before asyncio")

    await asyncio.sleep(2)

    print("After asyncio ")

myfunction()