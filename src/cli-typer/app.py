#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import platform
import time
from pathlib import Path
from typing import Optional

import typer

__version__ = "0.1.0"

app = typer.Typer(add_completion=True, no_args_is_help=True, help="""
Typer CLI example demonstrating:
- Global options via callback (verbosity, config, version)
- Multiple subcommands (run, greet, info)
- Error handling and basic diagnostics
""")


def _version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    verbose: int = typer.Option(0, "--verbose", "-v", count=True, help="Increase verbosity (repeatable)"),
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to a config file (INI/JSON/simple JSON lines)"),
    version: Optional[bool] = typer.Option(None, "--version", callback=_version_callback, is_eager=True, help="Show version and exit"),
):
    """Initialize shared state and parse global options.

    - Stores verbosity level and config path in ctx.obj
    - If --config is provided and exists, a best-effort JSON load is attempted
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["config_path"] = str(config) if config else None
    ctx.obj["config"] = None

    if config and config.exists():
        try:
            # Try JSON first; for real apps consider tomllib/yaml as needed
            ctx.obj["config"] = json.loads(Path(config).read_text())
        except Exception:
            # Keep going; config is optional in this demo
            pass


def _debug(ctx: typer.Context, msg: str) -> None:
    v = ctx.obj.get("verbose", 0) if ctx.obj else 0
    if v:
        typer.echo(f"[v{v}] {msg}", err=True)


@app.command()
def run(
    ctx: typer.Context,
    limit: int = typer.Option(5, min=0, help="Number of iterations to run"),
    delay: float = typer.Option(0.1, min=0.0, help="Seconds to sleep per step (simulated work)"),
    dry_run: bool = typer.Option(False, help="Plan only; do not perform the delay"),
):
    """Run a small loop to demonstrate options, validation, and logging."""
    _debug(ctx, f"Starting run: limit={limit}, delay={delay}, dry_run={dry_run}")
    for i in range(limit):
        typer.echo(f"typer: {i}")
        if not dry_run and delay:
            time.sleep(delay)
    _debug(ctx, "Run completed")


@app.command()
def greet(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Name to greet"),
    times: int = typer.Option(1, min=1, help="Repeat count"),
    loud: bool = typer.Option(False, help="Uppercase the greeting"),
):
    """Print a greeting, optionally repeated and uppercased."""
    _debug(ctx, f"Greeting name={name} times={times} loud={loud}")
    msg = f"Hello {name}"
    for _ in range(times):
        typer.echo(msg.upper() if loud else msg)


@app.command()
def info(
    ctx: typer.Context,
    json_out: bool = typer.Option(False, "--json", help="Emit machine-readable JSON"),
):
    """Show environment and configuration information."""
    data = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "cwd": str(Path.cwd()),
        "verbose": ctx.obj.get("verbose", 0) if ctx.obj else 0,
        "config_path": ctx.obj.get("config_path") if ctx.obj else None,
        "config": ctx.obj.get("config") if ctx.obj else None,
        "demo_api_key_set": bool(os.getenv("DEMO_API_KEY")),
    }
    if json_out:
        typer.echo(json.dumps(data))
    else:
        for k, v in data.items():
            typer.echo(f"{k}: {v}")


if __name__ == "__main__":
    app()
