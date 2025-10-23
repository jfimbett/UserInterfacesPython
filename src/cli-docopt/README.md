# docopt CLI Example

This example demonstrates a docopt-based CLI that contrasts a NORMAL path with a FAST path.

What does `--fast` do?
- Uses a smaller payload for hashing (1 KB vs 8 KB)
- Sleeps less per iteration to simulate lower latency (20ms vs 120ms)
- Finishes significantly faster; output is illustrative and may differ

Try it:

```bash
# NORMAL mode (default)
python app.py run --times=3

# FAST mode
python app.py run --fast --times=3

# Help and version
python app.py --help
python app.py --version
```

Sample output:

```
[NORMAL] iter=0 digest=ab12cd34 (payload=8000B, delay=120ms)
[NORMAL] iter=1 digest=ab12cd34 (payload=8000B, delay=120ms)
[NORMAL] iter=2 digest=ab12cd34 (payload=8000B, delay=120ms)

[FAST]   iter=0 digest=ef56aa99 (payload=1000B, delay=20ms)
[FAST]   iter=1 digest=ef56aa99 (payload=1000B, delay=20ms)
[FAST]   iter=2 digest=ef56aa99 (payload=1000B, delay=20ms)
```
