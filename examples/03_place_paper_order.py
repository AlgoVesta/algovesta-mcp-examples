"""Example 3: preview an order, then place it on the paper account with a stop-loss
and a take-profit. Running it twice with the same idempotency key places one order."""
import asyncio
import sys
import uuid

from common import VENUE, call, session, show

ORDER = {
    "venue": VENUE,             # paper: simulated balance, no real money
    "symbol": "BTCUSDT",
    "side": "buy",
    "order_type": "market",
    "size_usd": 50,             # position value in USD
    "sl_pct": 2,                # stop-loss 2 % below the fill
    "tp_pct": 4,                # take-profit 4 % above the fill
    "idempotency_key": sys.argv[1] if len(sys.argv) > 1 else "example-" + uuid.uuid4().hex[:12],
}


async def main():
    async with session() as s:
        preview = dict(ORDER, idempotency_key=ORDER["idempotency_key"] + "-preview")
        show("simulate_order (nothing is placed)", await call(s, "simulate_order", preview))
        show("place_order on paper", await call(s, "place_order", ORDER))


asyncio.run(main())
