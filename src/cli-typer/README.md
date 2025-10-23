# Typer CLI Example

This example demonstrates a more complete Typer CLI:

- Global options on the callback: `--verbose/-v` (repeatable), `--config/-c`, and `--version`
- Subcommands: `run`, `greet`, and `info`
- Shared state via `ctx.obj` and simple debug logging

## Try it

```bash
# Help and version
python app.py --help
python app.py --version

# Global verbosity and optional config
python app.py -vv --config sample.json info

# Run a loop (with simulated work)
python app.py run --limit 3 --delay 0.05
python app.py -v run --limit 3 --dry-run

# Greet
python app.py greet Alice --loud --times 2

# JSON info output
python app.py info --json
```

Notes:
- `-v` can be repeated for more debug output (printed to stderr).
- `--config` attempts to parse JSON (best effort) and makes it available under `ctx.obj['config']`.
