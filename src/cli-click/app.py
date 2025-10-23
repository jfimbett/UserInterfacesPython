#!/usr/bin/env python3
import os, click

@click.group()
@click.version_option("0.1.0")
@click.option("--verbose", "-v", count=True, help="Increase verbosity")
@click.pass_context
def cli(ctx, verbose):
    ctx.obj = {"verbose": verbose, "api_key": os.getenv("DEMO_API_KEY", "")}

# The 'run' command prints a numbered list up to the specified limit.
# If verbosity is enabled, it shows the API key status before printing.
@cli.command()
@click.option("--limit", default=5, show_default=True, type=int)
@click.option("--verbose", "-v", count=True, help="Increase verbosity")
@click.pass_context
def run(ctx, limit, verbose):
    # Support -v at both group and command level; combine them
    eff_v = (ctx.obj.get("verbose", 0) or 0) + (verbose or 0)
    if eff_v:
        click.echo(f"[v{eff_v}] api_key set? {bool(ctx.obj['api_key'])}")
    for i in range(limit):
        click.echo(f"click: {i}")

# The 'greet' command prompts the user for their name and prints a greeting in green and bold.
@cli.command()
@click.option("--name", prompt=True)
@click.option("--verbose", "-v", count=True, help="Increase verbosity")
@click.pass_context
def greet(ctx, name, verbose):
    eff_v = (ctx.obj.get("verbose", 0) or 0) + (verbose or 0)
    if eff_v:
        click.echo(f"[v{eff_v}] Greeting user…")
    click.secho(f"Hello {name}", fg="green", bold=True)

if __name__ == "__main__":
    cli()
