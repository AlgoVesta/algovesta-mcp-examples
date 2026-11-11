# AlgoVesta MCP examples (Python, paper mode)

Five small Python programs that call the [AlgoVesta MCP server](https://github.com/AlgoVesta/mcp) with the official `mcp` client library: connect, read a price, place an order with a stop-loss and a take-profit, change the stop-loss, and close the position. Every order goes to the **paper** account, a simulated balance; no real money is involved.

> Trading involves substantial risk of loss. Software, not advice.

## What do I need?

- Python 3.10 or newer.
- An AlgoVesta account and an MCP key with the `paper` scope. Create it in the dashboard under **MCP Connection**. New keys are `paper` by default; a `live` key needs a second factor and is not used here.

## How do I run the examples?

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and paste your paper key, or set the `ALGOVESTA_MCP_KEY` environment variable.
3. Run them in order from the repository root:

```
python examples/01_list_tools.py
python examples/02_get_price.py BTCUSDT
python examples/03_place_paper_order.py
python examples/04_positions_modify.py
python examples/05_close_position.py
```

## What does each example do?

| File | Tools it calls | Result |
|---|---|---|
| `01_list_tools.py` | `list_tools` | Prints every tool the server offers with its title. |
| `02_get_price.py` | `get_market_price` | The live price the server uses for a symbol, with the exchange, source and age. |
| `03_place_paper_order.py` | `simulate_order`, `place_order` | Shows the resolved order (entry, stop-loss, take-profit, size, policy verdict), then places a 50 USD BTCUSDT long on paper with a 2 % stop-loss and a 4 % take-profit. |
| `04_positions_modify.py` | `get_portfolio_context`, `modify_position` | Lists the paper positions and moves the stop-loss of the BTCUSDT long to 1.5 % below entry. |
| `05_close_position.py` | `close_position`, `get_trade_history` | Closes the BTCUSDT long and prints the last closed paper trades. |

`examples/common.py` holds the connection code: it reads the key, opens a Streamable HTTP session and decodes each tool result.

## Why does every call use `venue: "paper"`?

`common.VENUE` is `"paper"` and every order call in the examples passes it, so these programs cannot reach a connected exchange or MetaTrader 5 account. The scope of the key is a second limit: a `paper` key is refused by the server for anything that needs `live`. The CI check in `tests/test_offline.py` fails if an order call stops using the paper venue.

## Why does every order call send an `idempotency_key`?

The server performs an order, a change or a close once per key. If your program retries after a timeout with the same key, it gets the same result instead of a second order. `03_place_paper_order.py` accepts a key as its first argument so you can try this.

## What happens when an order breaks my risk rules?

The server checks every order against your account's risk policy (for example the required stop-loss, position caps and daily loss limit) and rejects it with the reason instead of changing it silently. `simulate_order` returns the same verdict without placing anything.

## Where are the tool descriptions?

In [AlgoVesta/mcp: docs/TOOLS.md](https://github.com/AlgoVesta/mcp/blob/main/docs/TOOLS.md), generated from the live server schema. Authentication options, including OAuth 2.1 for clients that prefer it, are in [docs/AUTHENTICATION.md](https://github.com/AlgoVesta/mcp/blob/main/docs/AUTHENTICATION.md).

## How are the examples tested?

- `python tests/test_offline.py` (CI, no key needed) compiles every example, checks that order calls use the paper venue, and checks that no real key is in the repository.
- The full run against the server with a paper key is repeated by the AlgoVesta team before each change and every six months.

## Related repositories

- [AlgoVesta/mcp](https://github.com/AlgoVesta/mcp): MCP server documentation.
- [AlgoVesta/algovesta-tradingview-templates](https://github.com/AlgoVesta/algovesta-tradingview-templates): TradingView webhook JSON templates and Pine Script examples.
- [AlgoVesta/algovesta-telegram-signal-formats](https://github.com/AlgoVesta/algovesta-telegram-signal-formats): Telegram signal formats the parser reads.

## License

MIT. See [LICENSE](LICENSE).
