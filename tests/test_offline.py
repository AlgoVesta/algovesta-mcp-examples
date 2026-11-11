"""Offline checks that run in CI without a key or a network connection.

Run: python tests/test_offline.py
- every example compiles;
- every call that can place, change or close an order uses the paper venue;
- no file in the repository contains a real key (the git-ignored .env is skipped).
Exit code 0 = all checks passed, 1 = at least one failure.
"""
import ast
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "examples")
ORDER_TOOLS = {"place_order", "simulate_order", "modify_position", "close_position",
               "cancel_order", "create_strategy", "update_strategy"}
failures = []


def check(ok, msg):
    if not ok:
        failures.append(msg)


common = ast.parse(open(os.path.join(EX, "common.py"), encoding="utf-8").read())
venue = [n.value.value for n in ast.walk(common) if isinstance(n, ast.Assign)
         and any(getattr(t, "id", "") == "VENUE" for t in n.targets)]
check(venue == ["paper"], "common.VENUE must be 'paper', got %r" % venue)

files = sorted(f for f in os.listdir(EX) if f.endswith(".py"))
check(len([f for f in files if f[:2].isdigit()]) == 5, "expected five numbered examples")
for name in files:
    src = open(os.path.join(EX, name), encoding="utf-8").read()
    try:
        tree = ast.parse(src)
        compile(src, name, "exec")
    except SyntaxError as e:
        check(False, "%s: %s" % (name, e))
        continue
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and getattr(node.func, "id", "") == "call"):
            continue
        tool = node.args[1].value if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) else None
        if tool not in ORDER_TOOLS:
            continue
        # the arguments must be a dict literal or a name bound to one, with venue=VENUE
        args = node.args[2] if len(node.args) > 2 else None
        text = ast.unparse(args) if args is not None else ""
        if isinstance(args, ast.Name) or isinstance(args, ast.Call):
            text = src
        check("'venue': VENUE" in text or '"venue": VENUE' in text,
              "%s: %s must use venue=VENUE (paper)" % (name, tool))

key = re.compile(r"avmcp_(?!<)[A-Za-z0-9_-]{20,}")
# Your local .env holds your real key on purpose and is git-ignored; it is skipped here.
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__"}
for base, dirs, names in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for n in names:
        if n == ".env":
            continue
        p = os.path.join(base, n)
        try:
            check(not key.search(open(p, encoding="utf-8").read()), "%s contains a key" % p)
        except (UnicodeDecodeError, PermissionError):
            pass

if failures:
    print("FAILED")
    for f in failures:
        print(" -", f)
    sys.exit(1)
print("OK: %d example files checked" % len(files))
