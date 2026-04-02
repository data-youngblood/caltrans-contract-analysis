-- Bid Items (item-level pricing from bid tabulation PDFs)
-- Source: Caltrans_Bid_Tab_PDF_to_CSV.py -> bid_items.csv
-- Join keys: contract_number, item_no
CREATE TABLE IF NOT EXISTS Caltrans.bid_items (
    contract_number     String,        -- joins to bid_summary
    bid_opening_date    String,
    district            String,
    item_no             String,        -- sequence number (001, 002, etc.)
    item_code           String,        -- Caltrans item code (e.g. "120090")
    item_description    String,
    unit                String,        -- unit of measure (LS, EA, TON, CY, etc.)
    estimated_quantity  Float64,
    unit_price          Float64,
    bid_amount          Float64,       -- quantity * unit_price
    bidder_type         String,        -- "LOW_BIDDER", "SECOND", "THIRD", etc.
    bidder_name         String,
    source_pdf          String
) ENGINE = MergeTree()
ORDER BY (contract_number, item_no, bidder_type);
