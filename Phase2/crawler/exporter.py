import csv
from pathlib import Path

def save_csv(rows, path, headers):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No rows to write – aborting CSV save.")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"[Done] Saved {len(rows)} rows → {path}")
