SKIPDIR = ["virtualenv", "node_modules", "__pycache__"]

import watchfiles
import asyncio

from .deploy import deploy
from .client import serve

async def loop():
    async for changes in watchfiles.awatch()

def watch():
    asyncio.run(loop())
    try:
        serve()
    except KeyboardInterrupt:
        print("Interrupted.")

    