-- Pay Estimate Items (item-level detail from PETS detail files)
-- Source: Caltrans_Pay_Estimate_Parser.py -> pay_estimate_items.csv
-- Join keys: contract_number, estimate_no, item_number
CREATE TABLE IF NOT EXISTS Caltrans.pay_estimate_items (
    contract_number     String,        -- joins to bid_summary, pay_estimates
    estimate_no         String,
    item_number         String,        -- 3-digit item sequence (001, 002, etc.)
    item_description    String,
    is_force_account    String,        -- 'Y' if force account item
    unit                String,
    contract_price      Float64,       -- unit price (4 decimal places)
    original_auth_amount Float64,      -- original authorized amount
    this_est_quantity   Float64,       -- quantity this estimate period
    this_est_amount     Float64,       -- amount this estimate period
    total_est_quantity  Float64,       -- cumulative quantity
    total_est_amount    Float64,       -- cumulative amount
    source_file         String
) ENGINE = MergeTree()
ORDER BY (contract_number, estimate_no, item_number);
