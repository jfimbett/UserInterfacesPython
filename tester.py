from rich.table import Table
from rich.console import Console

console = Console()
table = Table(title="Results")
for col in ("id", "score", "status"):
    table.add_column(col, justify="right")
for i in range(3):
    table.add_row(str(i), f"{0.9 - i*0.1:.2f}", "ok")
console.print(table)