# Caltrans Data Pipeline

Scrape, parse, and load California Department of Transportation (Caltrans) bid tabulation and pay estimate data into ClickHouse for analysis.

## Data Sources

| Source | URL | Data |
|--------|-----|------|
| Bid Tabulations | https://ppmoe.dot.ca.gov/cc?id=cc_bid_summary | Contract bids, bidder rankings, item-level pricing |
| Pay Estimates (PETS) | https://misc-external.dot.ca.gov/pets/ | Payment history, project status, item-level earned amounts |

## Project Structure

```
Caltrans-data/
├── Article/
│   ├── Caltrans_Article_Final.md              # Published article with analysis
│   └── Caltrans_Article_Statistic_Queries.md  # All backing SQL queries (Q1-Q31)
├── Scripts/
│   ├── Caltrans_Bid_Tab_Scraper.py            # Scrape bid tabulation PDFs (Selenium)
│   ├── Caltrans_Pay_Estimate_Scraper.py       # Scrape pay estimate Detail files (Selenium)
│   ├── Caltrans_Bid_Tab_PDF_to_CSV.py         # Parse bid tab PDFs -> CSV
│   ├── Caltrans_Pay_Estimate_Parser.py        # Parse pay estimate Detail files -> CSV
│   └── Clickhouse/
│       ├── load_all.py                        # Master loader (DDLs + truncate + all tables)
│       ├── load_bid_summary.py
│       ├── load_bid_items.py
│       ├── load_pay_estimates.py
│       ├── load_pay_estimate_items.py
│       └── load_payment_history.py
├── DDL/
│   ├── bid_summary.sql
│   ├── bid_items.sql
│   ├── pay_estimates.sql
│   ├── pay_estimate_items.sql
│   └── payment_history.sql
├── utils/
│   └── clickhouse_client.py                   # Shared CH connection + helpers
├── requirements.txt
├── README.md
└── TODO.md
```

## Data Flow

```
                     SCRAPE                          PARSE                         LOAD
                 ┌──────────────┐              ┌──────────────┐              ┌──────────────┐
Bid Summary  ──> │  Selenium    │ ── PDFs ──>  │  pdfplumber  │ ── CSVs ──> │  ClickHouse  │
(2019-present)   │  + requests  │              │  + OCR       │              │  Caltrans DB │
                 └──────────────┘              └──────────────┘              └──────────────┘
                 ┌──────────────┐              ┌──────────────┐              ┌──────────────┐
Pay Estimates -> │  Selenium    │ ── Detail -> │  Text parser │ ── CSVs ──> │  ClickHouse  │
(PETS portal)    │  + requests  │    files     │              │              │  Caltrans DB │
                 └──────────────┘              └──────────────┘              └──────────────┘
```

## NAS Storage Layout

```
\\192.168.50.100\pymedia\Data\California\CalTrans\
├── Bid_Tabulations/
│   ├── {year}/                    # PDFs organized by year (2019-2026)
│   ├── bid_summary.csv           # Parsed bid summary (15,847 rows)
│   ├── bid_items.csv             # Parsed item-level bids (1,063,890 rows)
│   └── Broken/                   # PDFs that failed to parse
└── Pay_Estimates/
    ├── Data/
    │   ├── {contract}/           # Detail estimate files per contract
    │   └── payment_history.csv   # Payment disbursement records (28,448 rows)
    └── Parsed/
        ├── pay_estimates.csv     # Parsed estimate summaries (27,303 rows)
        └── pay_estimate_items.csv # Parsed item-level details (2,299,213 rows)
```

## ClickHouse Schema

Database: `Caltrans` on `192.168.50.100:8123`

| Table | Purpose | Rows | Primary Key |
|-------|---------|------|-------------|
| `bid_summary` | All bidders per contract (rank, amount) | 15,847 (2,292 unique contracts) | contract_number, bid_rank |
| `bid_items` | Item-level pricing from all bidders | 1,063,890 | contract_number, item_no, bidder_type |
| `pay_estimates` | Estimate summaries (amounts, status, dates) | 27,303 | contract_number, estimate_no |
| `pay_estimate_items` | Item-level earned quantities/amounts | 2,299,213 | contract_number, estimate_no, item_number |
| `payment_history` | Disbursement/warrant data | 28,448 | contract_number, estimate_no |

**Total: 3,434,701 rows across 5 tables (2,292 unique contracts)**

> **Deduplication note:** `bid_summary` contains 733 duplicate rows from contracts parsed from multiple source PDFs. All queries must use `GROUP BY contract_number` with `any()` aggregation to get correct counts.

## Key Statistics (from Article — deduplicated)

| Metric | Value |
|--------|-------|
| Total unique contracts | 2,292 |
| Total awarded value | $19.25 billion |
| Average contract | $8.4 million |
| Largest contract | $274.9 million |
| FINAL contracts | 1,619 (from bid_summary join) / 1,644 (from pay_estimates) |
| Median cost overrun | +2.7% |
| Avg bidders/contract | 5.2 |
| Sole-bidder rate | 1.8% |
| Top contractor | Granite Construction ($1.69B, 147 wins) |
| Top highway | I-5 ($2.0B) |
| Top district | Bay Area ($3.25B) |
| Non-FINAL stale contracts (2019-2022) | 95 ($2.19B earned) |

## Loading

The loader uses **truncate-before-load** — if source CSVs exist, the table is truncated and reloaded. If no source files are found, the table is left untouched.

```bash
# Create database, tables, and load all data
python Scripts/Clickhouse/load_all.py
```

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Scrape (already done — data on NAS)
```bash
python Scripts/Caltrans_Bid_Tab_Scraper.py
python Scripts/Caltrans_Pay_Estimate_Scraper.py
```

### 3. Parse (already done — CSVs on NAS)
```bash
python Scripts/Caltrans_Bid_Tab_PDF_to_CSV.py
python Scripts/Caltrans_Pay_Estimate_Parser.py
```

### 4. Load into ClickHouse
```bash
python Scripts/Clickhouse/load_all.py
```

### 5. Run article queries
See `Article/Caltrans_Article_Statistic_Queries.md` for all SQL queries (Q1-Q31).

## Pipeline Status

| Component | Status | Notes |
|-----------|--------|-------|
| Bid Tab Scraper | Done | 2019-2026, all archived dates |
| Pay Estimate Scraper | Done | All contracts from bid tabulations |
| Bid Tab Parser | Done | 3,025 contracts parsed |
| Pay Estimate Parser | Done | 27,303 estimates parsed |
| ClickHouse Load | Done | 3.4M rows, truncate-reload |
| Article Queries (Q1-Q31) | Done | All results deduplicated and populated |
| Article Draft | In Progress | Needs update with deduplicated numbers |
| Non-FINAL Analysis | Done | 95 stale contracts analyzed |
| Data Quality Cleanup | Pending | Contractor name normalization, duplicate rows in source CSVs |
| Parser Update | Pending | Handle "RERUN PROGRESS ESTIMATE" status |
| Charts/Visualizations | Pending | |
| Publication | Pending | |
