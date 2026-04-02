"""Master loader: create Caltrans database, run DDLs, and load all tables.

Usage:
    python Scripts/Clickhouse/load_all.py
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.clickhouse_client import get_client, DATABASE

# DDL directory
DDL_DIR = Path(__file__).resolve().parent.parent.parent / "DDL"

# Import individual loaders
from Scripts.Clickhouse import (
    load_bid_summary,
    load_bid_items,
    load_pay_estimates,
    load_pay_estimate_items,
    load_payment_history,
)

LOADERS = [
    ("bid_summary", load_bid_summary.load),
    ("bid_items", load_bid_items.load),
    ("pay_estimates", load_pay_estimates.load),
    ("pay_estimate_items", load_pay_estimate_items.load),
    ("payment_history", load_payment_history.load),
]


def run_ddls(client):
    """Execute all DDL files to create tables."""
    sql_files = sorted(DDL_DIR.glob("*.sql"))
    for sql_file in sql_files:
        sql = sql_file.read_text(encoding="utf-8")
        # Execute each statement, stripping comment lines
        for stmt in sql.split(";"):
            # Remove comment-only lines before checking if statement is empty
            lines = [l for l in stmt.splitlines() if not l.strip().startswith("--")]
            cleaned = "\n".join(lines).strip()
            if not cleaned:
                continue
            try:
                client.command(cleaned)
                print(f"  DDL: {sql_file.name} ... OK")
            except Exception as e:
                print(f"  DDL: {sql_file.name} ... ERROR: {e}")


def main():
    start = time.time()

    print("=" * 70)
    print(f"  Caltrans Data Loader")
    print(f"  Database: {DATABASE}")
    print("=" * 70)

    # Step 1: Create database and tables
    print("\n  Creating database and tables...")
    client = get_client()
    run_ddls(client)

    # Step 2: Load data
    print("\n  Loading data...")
    results = []
    for name, loader in LOADERS:
        print(f"\n  --- {name} ---")
        try:
            count = loader()
            results.append((name, count, None))
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append((name, 0, str(e)))

    # Summary
    elapsed = time.time() - start
    print(f"\n{'=' * 70}")
    print(f"  Load complete in {elapsed:.1f}s")
    print(f"{'=' * 70}")
    for name, count, err in results:
        status = f"{count:,} rows" if not err else f"FAILED: {err}"
        print(f"  {name:30s} {status}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
