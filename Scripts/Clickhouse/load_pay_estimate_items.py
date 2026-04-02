"""Load pay_estimate_items.csv into Caltrans.pay_estimate_items."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.clickhouse_client import (
    get_client, find_csvs, load_csv, truncate_table, safe_float, safe_int, safe_str, DATABASE, NAS_BASE
)

TABLE = f"{DATABASE}.pay_estimate_items"
COLUMNS = [
    "contract_number", "estimate_no",
    "item_number", "item_description", "is_force_account",
    "unit", "contract_price",
    "original_auth_amount",
    "this_est_quantity", "this_est_amount",
    "total_est_quantity", "total_est_amount",
    "source_file",
]

EXPECTED_HEADERS = ["contract_number", "estimate_no", "item_number"]
SOURCE_DIR = os.path.join(NAS_BASE, "Pay_Estimates", "Parsed")


def row_parser(row):
    return [
        safe_str(row.get("contract_number")),
        safe_str(row.get("estimate_no")),
        safe_str(row.get("item_number")),
        safe_str(row.get("item_description")),
        safe_str(row.get("is_force_account")),
        safe_str(row.get("unit")),
        safe_float(row.get("contract_price")),
        safe_float(row.get("original_auth_amount")),
        safe_float(row.get("this_est_quantity")),
        safe_float(row.get("this_est_amount")),
        safe_float(row.get("total_est_quantity")),
        safe_float(row.get("total_est_amount")),
        safe_str(row.get("source_file")),
    ]


def load():
    client = get_client()
    csvs = find_csvs(SOURCE_DIR, EXPECTED_HEADERS)
    if not csvs:
        print("  pay_estimate_items: no source files found, skipping truncate")
        return 0
    truncate_table(client, TABLE)
    total = 0
    for csv_path in csvs:
        n = load_csv(client, TABLE, COLUMNS, csv_path, row_parser)
        total += n
        print(f"  pay_estimate_items: loaded {n} rows from {os.path.basename(csv_path)}")
    return total


if __name__ == "__main__":
    load()
