# This file is based on a python example of the Serenade protocol written by
# Tommy MacWilliam, available here:
# https://github.com/serenadeai/protocol/blob/master/python-editor/app.py

import asyncio
import json
import random
import traceback
import websockets
import sys
import logging
from os.path import expanduser


id = str(random.random())
websocket = None

app_name = 'Vim'
match_re = 'term'
websocket_address = 'ws://localhost:17373'

async def send(message, data):
    if not websocket:
        return

    await send_raw(json.dumps({"message": message, "data": data}))


async def send_raw(msg):
    if not websocket:
        return

    logging.info('Message: ' + msg)
    await websocket.send(msg)


async def send_heartbeat():
    # send a heartbeat every minute so that Serenade keeps the connection alive
    while True:
        if websocket:
            await send("heartbeat", {"id": id})

        await asyncio.sleep(60)

async def handle(message):
    logging.info('Received: ' + str(message))
    data = json.loads(message)["data"]

    # if Serenade doesn't have anything for us to execute, then we're done
    if "response" not in data or "execute" not in data["response"]:
        return

    output(message)


async def get_input():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return reader


async def read_input():
    reader = await get_input()

    while True:
        line = (await reader.readline()).decode().strip()

        logging.info('INPUT: ' + line)

        if not line.startswith('{'):
            if line == 'active':
                logging.info('Active')
                await send_active()
            else:
                logging.error('Unknown input: ' + line)

            continue

        try:
            await send_raw(line)
        except Exception as e:
            logging.error('Failed to send raw input: %s' % e)

def output(msg):
    sys.stdout.write(str(msg) + '\n')
    sys.stdout.flush()

async def send_active():
    await send(
        "active",
        {"id": id, "app": app_name, "match": match_re},
    )


async def handler():
    global websocket
    global id

    asyncio.create_task(send_heartbeat())
    asyncio.create_task(read_input())

    while True:
        try:
            async with websockets.connect(websocket_address) as ws:
                websocket = ws
                output("Connected")
                logging.info('Connected')

                await send_active()

                while True:
                    try:
                        message = await websocket.recv()
                        await handle(message)
                    except websockets.exceptions.ConnectionClosedError:
                        print("Disconnected")
                        logging.info('Disconnected')
                        websocket = None
                        break
        except OSError:
            websocket = None
            await asyncio.sleep(1)


if __name__ == "__main__":
    app_name = sys.argv[1]
    match_re = sys.argv[2]
    websocket_address = sys.argv[3]
    should_log = sys.argv[4]

    if should_log != '0':
        logging.basicConfig(
            filename=expanduser('~/.vim-serenade.log'),
            level=logging.INFO,
            format='%(asctime)s %(process)d %(levelname)-8s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

    output("Running")
    asyncio.get_event_loop().run_until_complete(handler())
