#!/usr/bin/env python3
import fire

class Tools:
    """Google Fire example: exposes methods as CLI commands"""
    def add(self, a: int, b: int) -> int:
        "This function adds two numbers"
        return a + b

    def greet(self, name: str = "World") -> str:
        return f"Hi {name}!"

if __name__ == "__main__":
    fire.Fire(Tools)
