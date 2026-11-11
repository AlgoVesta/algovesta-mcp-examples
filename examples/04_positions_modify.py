"""Example 4: list the paper positions and move the stop-loss of the BTCUSDT long."""
import asyncio
import uuid

from common import VENUE, call, session, show

SYMBOL = "BTCUSDT"


def paper_positions(portfolio):
    for acc in portfolio.get("accounts", []):
        if str(acc.get("venue", "")).lower() == VENUE:
            return acc.get("positions") or []
    return []


async def main():
    async with session() as s:
        positions = paper_positions(await call(s, "get_portfolio_context"))
        show("paper positions", positions)
        pos = next((p for p in positions
                    if p.get("symbol") == SYMBOL and p.get("side") == "long"), None)
        if not pos:
            print("No %s paper position. Run 03_place_paper_order.py first." % SYMBOL)
            return
        entry = float(pos["entry"])
        new_sl = round(entry * 0.985, 2)   # tighten the stop to 1.5 % below entry
        show("modify_position new_sl=%s" % new_sl, await call(s, "modify_position", {
            "venue": VENUE, "symbol": SYMBOL, "side": "buy", "new_sl": new_sl,
            "idempotency_key": "example-" + uuid.uuid4().hex[:12]}))


asyncio.run(main())
