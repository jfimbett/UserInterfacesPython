# Typer + Rich CLI Example

Summarize a CSV with progress and pretty output.

## Global options (apply to all commands)
- `-v/--verbose` (repeatable): show debug lines, e.g. `-vv`
- `--no-color`: disable ANSI colors (useful for logs/CI)
- `--width N`: override terminal width (40–240) for deterministic layout

## Run

```bash
# Basic
python app.py summarize sample.csv

# With global options
python app.py -v --no-color summarize sample.csv
python app.py --width 100 summarize sample.csv --delim ';'
```
