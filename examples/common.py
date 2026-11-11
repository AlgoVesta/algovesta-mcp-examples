"""Shared connection helper for the examples.

Reads the MCP key from the ALGOVESTA_MCP_KEY environment variable or from a .env
file next to the repository root. The key is never printed.
"""
import json
import os
import sys
from contextlib import asynccontextmanager

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# Every order in these examples goes to the simulated paper account.
VENUE = "paper"
SERVER = "https://api.algovesta.com/u/{key}/mcp"


def _read_key():
    key = os.environ.get("ALGOVESTA_MCP_KEY", "").strip()
    env = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if not key and os.path.exists(env):
        for line in open(env, encoding="utf-8"):
            name, _, value = line.strip().partition("=")
            if name == "ALGOVESTA_MCP_KEY":
                key = value.strip()
    if not key.startswith("avmcp_") or "<" in key:
        sys.exit("Set ALGOVESTA_MCP_KEY to a paper-scoped key (see .env.example).")
    return key


@asynccontextmanager
async def session():
    """Open an MCP session to the AlgoVesta server."""
    url = SERVER.format(key=_read_key())
    async with streamablehttp_client(url) as (read, write, _):
        async with ClientSession(read, write) as s:
            await s.initialize()
            yield s


async def call(s, tool, arguments=None):
    """Call a tool and return its result as a dict (or text when it is not JSON)."""
    result = await s.call_tool(tool, arguments or {})
    text = "".join(c.text for c in result.content if getattr(c, "type", "") == "text")
    try:
        data = json.loads(text)
    except ValueError:
        data = {"text": text}
    if result.isError:
        raise RuntimeError("%s failed: %s" % (tool, text))
    return data


def show(title, data):
    print("\n== %s" % title)
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
