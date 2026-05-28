import asyncio
from servers.search import search_web

async def test():
    result = await search_web("artificial intelligence")
    print(result)

asyncio.run(test())