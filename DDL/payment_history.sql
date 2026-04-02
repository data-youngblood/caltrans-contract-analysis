-- Payment History (disbursement/warrant data from PETS portal)
-- Source: Caltrans_Pay_Estimate_Scraper.py -> payment_history.csv
-- Join key: contract_number, estimate_no
CREATE TABLE IF NOT EXISTS Caltrans.payment_history (
    contract_number     String,        -- joins to bid_summary, pay_estimates
    estimate_no         String,        -- estimate sequence number
    type                String,        -- 'P/P', 'A/A', 'FIN'
    pmt_type            String,        -- 'warrant', 'eft', 'check'
    released_date       String,        -- MM/DD/YY or MM/DD/YYYY
    held                Float64,       -- amount held
    disbursed           Float64,       -- amount disbursed
    detail_filename     String,        -- detail file reference
    voucher_filename    String,        -- voucher file reference
    project_status      String         -- 'FINAL', 'AFTER ACCEPTANCE', 'PROGRESS'
) ENGINE = MergeTree()
ORDER BY (contract_number, estimate_no);
