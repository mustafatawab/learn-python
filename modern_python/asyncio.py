import asyncio
import time


async def function1():
    await asyncio.sleep(2)
    print("Function1")

async def function2():
    await asyncio.sleep(2)
    print("Function2")

async def function3():
    await asyncio.sleep(2)
    print("Function3")


async def main():
    await asyncio.gather(
        function1(),
     function2(),
     function3(),
    ) 

await main()
# asyncio.run(main())