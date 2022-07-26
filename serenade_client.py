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

icon = 'data:image/gif;base64,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'

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
    reader = asyncio.StreamReader(limit=1024*1024)
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


async def send_active(send_icon=False):
    msg = {
        "id": id,
        "app": app_name,
        "match": match_re,
    }

    if send_icon:
        msg["icon"] = icon

    await send("active", msg)


async def handler():
    global websocket
    global id

    asyncio.create_task(send_heartbeat())
    asyncio.create_task(read_input())

    while True:
        try:
            async with websockets.connect(websocket_address, max_size=10**9) as ws:
                websocket = ws
                output("Connected")
                logging.info('Connected')

                await send_active(True)

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
