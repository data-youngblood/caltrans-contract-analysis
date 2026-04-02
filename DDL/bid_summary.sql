-- Bid Summary (one row per bidder per contract, with contract metadata)
-- Source: Caltrans_Bid_Tab_PDF_to_CSV.py -> bid_summary.csv
-- Join key: contract_number
CREATE DATABASE IF NOT EXISTS Caltrans;

CREATE TABLE IF NOT EXISTS Caltrans.bid_summary (
    contract_number     String,        -- e.g. "07-0W3704" (district-contract)
    bid_opening_date    String,        -- YYYY-MM-DD
    district            String,        -- 2-digit district code
    project_id          String,
    location            String,
    contract_code       String,
    project_description String,
    number_of_items     String,
    number_of_bids      String,
    proposals_issued    String,
    working_days        String,
    engineer_estimate   Float64,
    overrun_underrun    String,        -- overrun/underrun amount (rank 1 vs engineer est)
    pct_over_under      String,        -- percentage over/under (rank 1 vs engineer est)
    federal_aid         String,
    bid_rank            UInt32,        -- bidder rank (1 = low bidder / winner)
    bid_amount          Float64,       -- total bid amount
    bidder_id           String,        -- Caltrans bidder/vendor ID
    bidder_name         String,
    preference          String,        -- bid preference info
    source_pdf          String
) ENGINE = MergeTree()
ORDER BY (contract_number, bid_rank);
