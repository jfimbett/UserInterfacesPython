#!/usr/bin/env python3
from time import sleep
from tqdm import tqdm

# Basic iteration
for i in tqdm(range(200), desc="Loop"):
    sleep(0.005)

# Manual mode
from tqdm import tqdm as tq
with tq(total=50, desc="Manual") as bar:
    for _ in range(10):
        sleep(0.02)
        bar.update(5)
