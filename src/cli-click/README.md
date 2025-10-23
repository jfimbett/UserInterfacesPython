# Click CLI Example

Run:

```bash
# Show help
python app.py --help

# You can pass -v either before or after the subcommand
python app.py -v run --limit 3
python app.py run --limit 3 -v

# Double-verbose
DEMO_API_KEY=secret python app.py -vv run --limit 2
DEMO_API_KEY=secret python app.py run --limit 2 -vv

# Greet (prompts for name); -v also supported
python app.py greet
python app.py greet -v
```

Notes:
- Group-level options (like -v) usually come before the subcommand in Click; this example also accepts -v at the subcommand level for convenience.
- The demo checks an env var (DEMO_API_KEY) and shows its presence when verbose is enabled.
