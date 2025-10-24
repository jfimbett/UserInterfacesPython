#!/usr/bin/env python3
import sys
from datetime import datetime
import click

try:
    import yfinance as yf
except Exception as e:
    raise SystemExit("This tool requires the 'yfinance' package. Install it with: pip install yfinance")

def function(arg1, arg2, arg3, keyword=True):
    pass

@click.command()
@click.argument("ticker")
@click.option(
    "--start",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Start date (YYYY-MM-DD)."
)
@click.option(
    "--end",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="End date (YYYY-MM-DD)."
)
@click.option(
    "--period",
    type=click.Choice(["1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"]),
    default="1y",
    show_default=True,
    help="Used if --start/--end are not provided."
)
@click.option(
    "--interval",
    type=click.Choice(["1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"]),
    default="1d",
    show_default=True,
    help="Data interval."
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False, writable=True, allow_dash=True),
    default="-",
    show_default=True,
    help="Output file path, or '-' for stdout."
)
@click.option(
    "--format",
    "fmt",
    type=click.Choice(["csv","json"]),
    default="csv",
    show_default=True,
    help="Output format."
)
@click.option(
    "--adjust/--no-adjust",
    default=True,
    show_default=True,
    help="Whether to auto-adjust OHLC for splits/dividends."
)
def main(ticker, start, end, period, interval, output, fmt, adjust):
    """
    Download historical data for TICKER from Yahoo Finance and save to a file (or stdout).
    """
    # Validate mutually exclusive options
    if (start or end) and period:
        # If any date is provided, ignore period to avoid confusion
        period = None

    # Convert click.DateTime -> date string for yfinance
    start_str = start.date().isoformat() if start else None
    end_str = end.date().isoformat() if end else None

    # Fetch data
    click.echo(f"Downloading {ticker} (interval={interval})...", err=True)
    try:
        df = yf.download(
            tickers=ticker,
            start=start_str,
            end=end_str,
            period=period,
            interval=interval,
            auto_adjust=adjust,
            progress=False,
            threads=False,
        )
    except Exception as e:
        raise click.ClickException(f"Failed to download data: {e}")

    if df is None or df.empty:
        raise click.ClickException("No data returned. Check the ticker, dates, or interval.")

    # Ensure a clean tabular output (include the date as a column)
    df = df.copy()
    df.index.name = "Date"
    df.reset_index(inplace=True)

    # Serialize
    try:
        if fmt == "csv":
            payload = df.to_csv(index=False)
        else:
            payload = df.to_json(orient="records", date_format="iso")
    except Exception as e:
        raise click.ClickException(f"Failed to serialize data: {e}")

    # Write to file or stdout
    if output == "-":
        # Use click.echo for proper stdout handling (no color)
        click.echo(payload, nl=True)
    else:
        try:
            with open(output, "w", encoding="utf-8") as f:
                f.write(payload)
            click.secho(f"Saved to {output}", fg="green", err=True)
        except Exception as e:
            raise click.ClickException(f"Failed to write output: {e}")

if __name__ == "__main__":
    main()
