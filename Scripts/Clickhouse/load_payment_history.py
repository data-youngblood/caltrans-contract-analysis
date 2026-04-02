"""Load payment_history.csv into Caltrans.payment_history."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.clickhouse_client import (
    get_client, find_csvs, load_csv, truncate_table, safe_float, safe_str, DATABASE, NAS_BASE
)

TABLE = f"{DATABASE}.payment_history"
COLUMNS = [
    "contract_number", "estimate_no", "type", "pmt_type",
    "released_date", "held", "disbursed",
    "detail_filename", "voucher_filename",
    "project_status",
]

EXPECTED_HEADERS = ["contract_number", "estimate_no", "type"]
SOURCE_DIR = os.path.join(NAS_BASE, "Pay_Estimates", "Data")


def row_parser(row):
    return [
        safe_str(row.get("contract_number")),
        safe_str(row.get("estimate_no")),
        safe_str(row.get("type")),
        safe_str(row.get("pmt_type")),
        safe_str(row.get("released_date")),
        safe_float(row.get("held")),
        safe_float(row.get("disbursed")),
        safe_str(row.get("detail_filename")),
        safe_str(row.get("voucher_filename")),
        safe_str(row.get("project_status")),
    ]


def load():
    client = get_client()
    csvs = find_csvs(SOURCE_DIR, EXPECTED_HEADERS)
    if not csvs:
        print("  payment_history: no source files found, skipping truncate")
        return 0
    truncate_table(client, TABLE)
    total = 0
    for csv_path in csvs:
        n = load_csv(client, TABLE, COLUMNS, csv_path, row_parser)
        total += n
        print(f"  payment_history: loaded {n} rows from {os.path.basename(csv_path)}")
    return total


if __name__ == "__main__":
    load()
