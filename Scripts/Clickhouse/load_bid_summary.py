"""Load bid_summary.csv into Caltrans.bid_summary."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.clickhouse_client import (
    get_client, find_csvs, load_csv, truncate_table, safe_float, safe_int, safe_str, DATABASE, NAS_BASE
)

TABLE = f"{DATABASE}.bid_summary"
COLUMNS = [
    "contract_number", "bid_opening_date", "district",
    "project_id", "location", "contract_code",
    "project_description",
    "number_of_items", "number_of_bids", "proposals_issued",
    "working_days",
    "engineer_estimate",
    "overrun_underrun", "pct_over_under",
    "federal_aid",
    "bid_rank", "bid_amount", "bidder_id", "bidder_name",
    "preference",
    "source_pdf",
]

EXPECTED_HEADERS = ["contract_number", "bid_opening_date", "bid_rank", "bidder_name"]
SOURCE_DIR = os.path.join(NAS_BASE, "Bid_Tabulations")


def row_parser(row):
    return [
        safe_str(row.get("contract_number")),
        safe_str(row.get("bid_opening_date")),
        safe_str(row.get("district")),
        safe_str(row.get("project_id")),
        safe_str(row.get("location")),
        safe_str(row.get("contract_code")),
        safe_str(row.get("project_description")),
        safe_str(row.get("number_of_items")),
        safe_str(row.get("number_of_bids")),
        safe_str(row.get("proposals_issued")),
        safe_str(row.get("working_days")),
        safe_float(row.get("engineer_estimate")),
        safe_str(row.get("overrun_underrun")),
        safe_str(row.get("pct_over_under")),
        safe_str(row.get("federal_aid")),
        safe_int(row.get("bid_rank")),
        safe_float(row.get("bid_amount")),
        safe_str(row.get("bidder_id")),
        safe_str(row.get("bidder_name")),
        safe_str(row.get("preference")),
        safe_str(row.get("source_pdf")),
    ]


def load():
    client = get_client()
    csvs = find_csvs(SOURCE_DIR, EXPECTED_HEADERS)
    if not csvs:
        print("  bid_summary: no source files found, skipping truncate")
        return 0
    truncate_table(client, TABLE)
    total = 0
    for csv_path in csvs:
        n = load_csv(client, TABLE, COLUMNS, csv_path, row_parser)
        total += n
        print(f"  bid_summary: loaded {n} rows from {os.path.basename(csv_path)}")
    return total


if __name__ == "__main__":
    load()
