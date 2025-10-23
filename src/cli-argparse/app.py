#!/usr/bin/env python3
"""Argparse CLI example with subcommands.
Usage:
  python app.py run --limit 10
  python app.py info --json
"""
import argparse, json, sys

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="argcli", description="Argparse demo")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="Run a computation")
    p_run.add_argument("--limit", type=int, default=5, help="Number of items")

    p_info = sub.add_parser("info", help="Show info")
    p_info.add_argument("--json", action="store_true", help="Output JSON")
    return parser

def cmd_run(limit: int) -> int:
    for i in range(limit):
        print(f"processing {i}")
    return 0

def cmd_info(as_json: bool) -> int:
    data = {"python": sys.version.split()[0], "argv": sys.argv[1:]}
    if as_json:
        print(json.dumps(data))
    else:
        print("python:", data["python"]) ; print("argv:", data["argv"]) 
    return 0

def main() -> int:
    args = build_parser().parse_args()
    if args.cmd == "run":
        return cmd_run(args.limit)
    if args.cmd == "info":
        return cmd_info(args.json)
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
