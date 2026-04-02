"""Load bid_items.csv into Caltrans.bid_items."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.clickhouse_client import (
    get_client, find_csvs, load_csv, truncate_table, safe_float, safe_int, safe_str, DATABASE, NAS_BASE
)

TABLE = f"{DATABASE}.bid_items"
COLUMNS = [
    "contract_number", "bid_opening_date", "district",
    "item_no", "item_code", "item_description",
    "unit", "estimated_quantity",
    "unit_price", "bid_amount",
    "bidder_type", "bidder_name",
    "source_pdf",
]

EXPECTED_HEADERS = ["contract_number", "item_no", "unit_price", "bidder_type"]
SOURCE_DIR = os.path.join(NAS_BASE, "Bid_Tabulations")


def row_parser(row):
    return [
        safe_str(row.get("contract_number")),
        safe_str(row.get("bid_opening_date")),
        safe_str(row.get("district")),
        safe_str(row.get("item_no")),
        safe_str(row.get("item_code")),
        safe_str(row.get("item_description")),
        safe_str(row.get("unit")),
        safe_float(row.get("estimated_quantity")),
        safe_float(row.get("unit_price")),
        safe_float(row.get("bid_amount")),
        safe_str(row.get("bidder_type")),
        safe_str(row.get("bidder_name")),
        safe_str(row.get("source_pdf")),
    ]


def load():
    client = get_client()
    csvs = find_csvs(SOURCE_DIR, EXPECTED_HEADERS)
    if not csvs:
        print("  bid_items: no source files found, skipping truncate")
        return 0
    truncate_table(client, TABLE)
    total = 0
    for csv_path in csvs:
        n = load_csv(client, TABLE, COLUMNS, csv_path, row_parser)
        total += n
        print(f"  bid_items: loaded {n} rows from {os.path.basename(csv_path)}")
    return total


if __name__ == "__main__":
    load()
