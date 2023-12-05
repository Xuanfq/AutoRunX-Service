#!/usr/bin/env python

import asyncio
import websockets
import pymysql

async def hello():
    ACCEPT_SIGNAL = '^^^^^^^^^^ACCEPT^^^^^^^^^^'
    REFUSE_SIGNAL = '^^^^^^^^^^REFUSE^^^^^^^^^^'
    uri = "ws://localhost:8765/api/app/appmonitor/adf77578-1e50-484b-b717-24fe5281e245"
    async with websockets.connect(uri) as websocket:
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MDE5NjU1NDguNTc5ODYwNywiaWF0IjoxNzAxMzYwNzQ4LjU3OTg2MTQsImlzcyI6IkF1dG9SdW5YIiwiZGF0YSI6eyJ1c2VybmFtZSI6ImFkbWluIn19.wyUXrkweYaOq8x-k73wKH_F5wVntb1NHFvLFKwTBBU4'
        await websocket.send(token)
        result = await websocket.recv()
        print(result)
        # while True:
        #     data = input("> ")
        #     await websocket.send(data)
        #     result = await websocket.recv()
        #     print(result)
        # await websocket.send('appmonitor adf77578-1e50-484b-b717-24fe5281e245')
        async for message in websocket:
            print(message,end='')
        print()

if __name__ == "__main__":
    asyncio.run(hello())
