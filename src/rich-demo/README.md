# Rich Demo — Market Data Mini-App

Interactive terminal UI using Rich:
- Pick a ticker from a short list (AAPL, MSFT, GOOG, AMZN, NVDA)
- Choose start/end dates (defaults to the last 1 year)
- Downloads prices via `yfinance`
- Computes expected annual return and annual volatility (from daily returns)
- Shows metrics and a table with the last 5 closing prices

Requirements: `pip install -r ../../requirements.txt`

Run:

```bash
python app.py
```

Notes:
- Annual return ~ mean(daily returns) × 252; annual volatility ~ std(daily returns) × sqrt(252).