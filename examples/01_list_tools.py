"""Example 1: connect and list the tools the server offers."""
import asyncio

from common import session


async def main():
    async with session() as s:
        tools = (await s.list_tools()).tools
        print("Connected. %d tools:" % len(tools))
        for t in tools:
            title = t.annotations.title if t.annotations else ""
            print("  %-30s %s" % (t.name, title or ""))


asyncio.run(main())
