#!/usr/bin/env python3
from __future__ import annotations

from datetime import date, timedelta
from time import sleep
from typing import Tuple

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich.prompt import Prompt

console = Console()


def pick_inputs() -> Tuple[str, str, str]:
    """Prompt user for ticker and date range with sensible defaults."""
    tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA"]
    ticker = Prompt.ask("[bold cyan]Choose ticker[/]", choices=tickers, default=tickers[0])

    end_default = date.today()
    start_default = end_default - timedelta(days=365)
    start = Prompt.ask("Start date (YYYY-MM-DD)", default=start_default.isoformat())
    end = Prompt.ask("End date (YYYY-MM-DD)", default=end_default.isoformat())
    return ticker, start, end


def download_prices(ticker: str, start: str, end: str) -> pd.DataFrame:
    try:
        import yfinance as yf
    except Exception as e:
        console.print("[red]yfinance is required. Install with[/] [yellow]pip install -r requirements.txt[/]")
        raise

    with console.status(f"Downloading [bold]{ticker}[/] prices…", spinner="dots"):
        df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
        sleep(0.2)  # tiny pause for UX polish
    if df.empty:
        raise ValueError("No data returned; check ticker and dates.")
    return df


def compute_metrics(df: pd.DataFrame, ticker: str) -> Tuple[float, float, int]:
    """Return (annual_return, annual_volatility, observations) as floats.

    Handles yfinance returning MultiIndex columns by selecting the requested ticker
    or the first available column under "Close".
    """
    close = df["Close"]
    # If yfinance returns a DataFrame for df["Close"], pick the ticker column if present
    if isinstance(close, pd.DataFrame):
        if ticker in getattr(close, "columns", []):
            close = close[ticker]
        else:
            close = close.iloc[:, 0]
    close = close.dropna()

    rets = close.pct_change().dropna()
    n = int(len(rets))
    if n == 0:
        raise ValueError("Not enough data to compute returns.")
    # Convert to native floats to avoid pandas Series/NumPy scalar surprises
    ann_ret = float(rets.mean()) * 252.0
    ann_vol = float(rets.std()) * (252.0 ** 0.5)
    return ann_ret, ann_vol, n


def render_summary(ticker: str, start: str, end: str, df: pd.DataFrame, ann_ret: float, ann_vol: float, n: int) -> None:
    console.print(Panel.fit(f"[bold cyan]Market Data Summary[/] for [bold]{ticker}[/]"))

    # Metrics panel
    metrics = Table.grid(expand=False)
    metrics.add_column(justify="right")
    metrics.add_column(justify="left")
    # Use ASCII-only characters to avoid encoding issues on some terminals
    metrics.add_row("Period:", f"{start} to {end}")
    metrics.add_row("Observations:", str(n))
    metrics.add_row("Ann. Return:", f"{ann_ret*100:.2f}%")
    metrics.add_row("Ann. Volatility:", f"{ann_vol*100:.2f}%")
    # Simple Sharpe approximation (rf≈0)
    sharpe = (ann_ret / ann_vol) if ann_vol else float("nan")
    metrics.add_row("Sharpe (rf~0):", f"{sharpe:.2f}")
    console.print(Panel(metrics, title="Metrics", expand=False))

    # Sample prices (robust to yfinance multi-ticker frames)
    tbl = Table(title="Sample closing prices (last 5)")
    tbl.add_column("Date")
    tbl.add_column("Close", justify="right")

    # Prefer the selected ticker if df["Close"] is a DataFrame, else use the Series
    close_col = df.get("Close") if hasattr(df, "get") else df["Close"]
    if isinstance(close_col, pd.DataFrame):
        if ticker in close_col.columns:
            close_series = close_col[ticker]
        else:
            # Fallback to the first available column
            close_series = close_col.iloc[:, 0]
    else:
        close_series = close_col

    tail_series = close_series.dropna().tail(5)
    for idx, val in tail_series.items():
        ts = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)
        try:
            num = float(val)
        except Exception:
            num = val
        tbl.add_row(ts, f"{num:.2f}" if isinstance(num, float) else str(num))
    console.print(tbl)


def main() -> None:
    console.print(Panel.fit("[bold cyan]Rich[/] demo: pick a ticker, fetch prices, compute [green]annual return[/] and [yellow]volatility[/]."))
    ticker, start, end = pick_inputs()
    try:
        df = download_prices(ticker, start, end)
        ann_ret, ann_vol, n = compute_metrics(df, ticker)
    except Exception as e:
        console.print(f"[red]Error:[/] {e}")
        return
    render_summary(ticker, start, end, df, ann_ret, ann_vol, n)


if __name__ == "__main__":
    main()
