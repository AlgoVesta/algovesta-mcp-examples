"""Example 2: read the live price the server uses for a symbol.

No venue is passed, so the server looks the symbol up on your connected exchanges
(Binance when none is connected) and says which exchange and source it used."""
import asyncio
import sys

from common import call, session, show

SYMBOL = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"


async def main():
    async with session() as s:
        show("get_market_price %s" % SYMBOL,
             await call(s, "get_market_price", {"symbol": SYMBOL}))


asyncio.run(main())
