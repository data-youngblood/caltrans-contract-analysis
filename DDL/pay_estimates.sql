-- Pay Estimates (one row per contract estimate from PETS detail files)
-- Source: Caltrans_Pay_Estimate_Parser.py -> pay_estimates.csv
-- Join key: contract_number, estimate_no
CREATE TABLE IF NOT EXISTS Caltrans.pay_estimates (
    contract_number              String,        -- joins to bid_summary
    estimate_no                  String,        -- estimate sequence number
    project_status               String,        -- 'FINAL', 'PROGRESS', 'AFTER ACCEPTANCE'
    estimate_type                String,        -- 'P/P', 'A/A', 'FIN'
    district                     String,
    contractor_name              String,
    contractor_address           String,
    location                     String,
    project_description          String,
    re_name                      String,        -- Resident Engineer
    bid_opening_date             String,        -- MM/DD/YY
    estimate_date                String,        -- MM/DD/YY
    work_performed_through       String,        -- MM/DD/YY
    federal_aid                  String,
    original_contract_amount     Float64,
    current_contract_amount      Float64,
    subtotal_without_mobilization Float64,
    adjustment_of_compensation   Float64,
    extra_work                   Float64,
    mobilization_amount          Float64,
    total_work_completed         Float64,
    total_work_completed_this_est Float64,
    materials_on_hand            Float64,
    deductions                   Float64,
    total_earned                 Float64,
    total_earned_this_est        Float64,
    date_approved                String,        -- MM/DD/YY
    contract_days                String,
    date_work_started            String,        -- MM/DD/YY
    begin_construction           String,        -- MM/DD/YY
    completion_date              String,        -- MM/DD/YY (estimated or actual)
    working_days_charged         String,
    weather_days                 String,
    cco_days                     String,
    other_days                   String,
    percent_complete             String,
    percent_time_elapsed         String,
    source_file                  String
) ENGINE = MergeTree()
ORDER BY (contract_number, estimate_no);
