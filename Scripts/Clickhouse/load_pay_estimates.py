"""Load pay_estimates.csv into Caltrans.pay_estimates."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from utils.clickhouse_client import (
    get_client, find_csvs, load_csv, truncate_table, safe_float, safe_int, safe_str, DATABASE, NAS_BASE
)

TABLE = f"{DATABASE}.pay_estimates"
COLUMNS = [
    "contract_number", "estimate_no", "project_status",
    "estimate_type", "district",
    "contractor_name", "contractor_address",
    "location", "project_description", "re_name",
    "bid_opening_date", "estimate_date", "work_performed_through",
    "federal_aid",
    "original_contract_amount", "current_contract_amount",
    "subtotal_without_mobilization", "adjustment_of_compensation",
    "extra_work", "mobilization_amount",
    "total_work_completed", "total_work_completed_this_est",
    "materials_on_hand", "deductions",
    "total_earned", "total_earned_this_est",
    "date_approved", "contract_days",
    "date_work_started", "begin_construction",
    "completion_date",
    "working_days_charged", "weather_days", "cco_days", "other_days",
    "percent_complete", "percent_time_elapsed",
    "source_file",
]

EXPECTED_HEADERS = ["contract_number", "estimate_no", "project_status"]
SOURCE_DIR = os.path.join(NAS_BASE, "Pay_Estimates", "Parsed")


def row_parser(row):
    return [
        safe_str(row.get("contract_number")),
        safe_str(row.get("estimate_no")),
        safe_str(row.get("project_status")),
        safe_str(row.get("estimate_type")),
        safe_str(row.get("district")),
        safe_str(row.get("contractor_name")),
        safe_str(row.get("contractor_address")),
        safe_str(row.get("location")),
        safe_str(row.get("project_description")),
        safe_str(row.get("re_name")),
        safe_str(row.get("bid_opening_date")),
        safe_str(row.get("estimate_date")),
        safe_str(row.get("work_performed_through")),
        safe_str(row.get("federal_aid")),
        safe_float(row.get("original_contract_amount")),
        safe_float(row.get("current_contract_amount")),
        safe_float(row.get("subtotal_without_mobilization")),
        safe_float(row.get("adjustment_of_compensation")),
        safe_float(row.get("extra_work")),
        safe_float(row.get("mobilization_amount")),
        safe_float(row.get("total_work_completed")),
        safe_float(row.get("total_work_completed_this_est")),
        safe_float(row.get("materials_on_hand")),
        safe_float(row.get("deductions")),
        safe_float(row.get("total_earned")),
        safe_float(row.get("total_earned_this_est")),
        safe_str(row.get("date_approved")),
        safe_str(row.get("contract_days")),
        safe_str(row.get("date_work_started")),
        safe_str(row.get("begin_construction")),
        safe_str(row.get("completion_date")),
        safe_str(row.get("working_days_charged")),
        safe_str(row.get("weather_days")),
        safe_str(row.get("cco_days")),
        safe_str(row.get("other_days")),
        safe_str(row.get("percent_complete")),
        safe_str(row.get("percent_time_elapsed")),
        safe_str(row.get("source_file")),
    ]


def load():
    client = get_client()
    csvs = find_csvs(SOURCE_DIR, EXPECTED_HEADERS)
    if not csvs:
        print("  pay_estimates: no source files found, skipping truncate")
        return 0
    truncate_table(client, TABLE)
    total = 0
    for csv_path in csvs:
        n = load_csv(client, TABLE, COLUMNS, csv_path, row_parser)
        total += n
        print(f"  pay_estimates: loaded {n} rows from {os.path.basename(csv_path)}")
    return total


if __name__ == "__main__":
    load()
