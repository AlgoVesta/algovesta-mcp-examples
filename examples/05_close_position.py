"""Example 5: close the BTCUSDT paper long and show the closed trade."""
import asyncio
import uuid

from common import VENUE, call, session, show

SYMBOL = "BTCUSDT"


async def main():
    async with session() as s:
        show("close_position", await call(s, "close_position", {
            "venue": VENUE, "symbol": SYMBOL, "side": "buy", "fraction": 1,
            "idempotency_key": "example-" + uuid.uuid4().hex[:12]}))
        show("get_trade_history (paper, last 5)",
             await call(s, "get_trade_history", {"venue": VENUE, "limit": 5}))


asyncio.run(main())
