#!/usr/bin/env python3
import csv, typer
from rich.table import Table
from rich.console import Console
from rich.progress import track

app = typer.Typer()
console = Console()

def _debug(ctx: typer.Context, msg: str) -> None:
    v = (ctx.obj or {}).get("verbose", 0)
    if v:
        console.print(f"[dim]v{v}[/] {msg}", highlight=False)

@app.callback()
def main(
    ctx: typer.Context,
    verbose: int = typer.Option(0, "--verbose", "-v", count=True, help="Increase verbosity (repeatable)"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable ANSI colors in output"),
    width: int = typer.Option(None, "--width", min=40, max=240, help="Override terminal width for rendering"),
):
    """Typer + Rich demo CLI (group).

    Sets global options for the whole app and configures Rich accordingly.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose

    # Reconfigure the global Console with requested options
    global console
    console = Console(no_color=no_color, width=width)
    _debug(ctx, f"Console configured (no_color={no_color}, width={width})")

@app.command()
def summarize(ctx: typer.Context, path: str, delim: str = ","):
    """Summarize a CSV file: number of rows and show first row."""
    _debug(ctx, f"Summarizing path='{path}' delim='{delim}'")
    try:
        rows = list(track(csv.DictReader(open(path), delimiter=delim), description="Reading"))
    except FileNotFoundError:
        console.print("[red]File not found[/]")
        raise typer.Exit(code=2)
    table = Table(title="Summary")
    table.add_column("rows")
    table.add_column("columns")
    n_rows = len(rows)
    n_cols = len(rows[0].keys()) if rows else 0
    table.add_row(str(n_rows), str(n_cols))
    console.print(table)
    if rows:
        console.rule("First Row")
        t2 = Table(*rows[0].keys(), title="Row 0")
        t2.add_row(*[str(v) for v in rows[0].values()])
        console.print(t2)

import time 
from rich.progress import Progress
@app.command()
def longfunction(ctx: typer.Context):
    """This is a very long function with progress tracking."""
    _debug(ctx, "Starting long function")
    
    
    with Progress(console=console) as progress:
        task = progress.add_task("[cyan]Processing...", total=10)
        for i in range(10):
            time.sleep(1)
            progress.update(task, advance=1)
    
    console.print("[green]✓[/green] Long function completed!")



if __name__ == "__main__":
    app()
