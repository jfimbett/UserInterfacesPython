#!/usr/bin/env python3
"""
Demo CLI using docopt that contrasts a "normal" path with a "fast" path.

Usage:
  app.py run [--fast] [--times=N]
  app.py (-h | --help)
  app.py --version

Options:
  -h --help       Show this screen.
  --version       Show version.
  --fast          Fast mode: uses a lighter workload and shorter delay per step
                  to minimize latency (useful for demos). Output is illustrative
                  and may differ from normal mode.
  --times=N       Number of iterations to run [default: 3].

Details:
  Normal mode simulates a heavier task by hashing a larger payload and adding a
  longer sleep per iteration to mimic I/O or network latency.
  Fast mode uses a smaller payload and a shorter sleep to finish faster.
"""
from docopt import docopt
from hashlib import sha256
import time

VERSION = "1.0.0"

def main():
    args = docopt(__doc__, version=VERSION)
    times = int(args["--times"]) if args["--times"] else 3
    fast = bool(args["--fast"])  # True if --fast provided

    def compute_digest(i: int, fast: bool) -> str:
        # Simulate different workloads by changing payload size and sleep.
        payload_len = 1_000 if fast else 8_000
        delay = 0.02 if fast else 0.12
        payload = ("x" * payload_len).encode()
        digest = sha256(payload).hexdigest()[:8]
        time.sleep(delay)
        return digest

    for i in range(times):
        digest = compute_digest(i, fast)
        mode = "FAST" if fast else "NORMAL"
        print(f"[{mode}] iter={i} digest={digest} (payload={1000 if fast else 8000}B, delay={'20ms' if fast else '120ms'})")

if __name__ == "__main__":
    main()
