# Caltrans Non-FINAL Contract Analysis

**Analysis Date:** 2026-03-22
**Database:** ClickHouse at `192.168.50.100:8123`, database `Caltrans`

## Overview

Of 2,292 unique Caltrans contracts (2019-2026), **469 contracts lack a FINAL pay estimate**. This analysis focuses on the 95 contracts from 2019-2022 that are still in PROGRESS or AFTER ACCEPTANCE status — contracts that are 3-7 years old and should have been completed by now.

### Status Breakdown (All Non-FINAL Contracts)

| Status | Contracts | Total Original | Total Earned | Avg % Complete |
|---|---|---|---|---|
| PROGRESS | 392 | $6,971,740,442 | $4,874,356,837 | 66% |
| AFTER ACCEPTANCE | 77 | $601,551,647 | $630,767,151 | 100% |
| **Total** | **469** | **$7,573,292,089** | **$5,505,123,988** | |

> AFTER ACCEPTANCE contracts at 100% completion are likely waiting on paperwork/final accounting. PROGRESS contracts are the concerning ones.

---

## 95 Stale Contracts (2019-2022, No FINAL)

### Summary Statistics

| Metric | Value |
|---|---|
| Contracts | 95 |
| Avg Original Amount | $22,318,710 |
| Avg Total Earned | $23,080,010 |
| Avg Overrun % | -0.5% (median +1.6%) |
| Total Original Value | $2,120,277,406 |
| Total Earned So Far | $2,192,600,991 |
| Total Overrun | $72,323,586 |
| Avg Working Days Charged | 410 |
| Avg Contract Days Allowed | 533 |
| Over Time (days) | 23 contracts (24.2%) |
| Over Budget (dollars) | 51 contracts (53.7%) |

### Contract Size Distribution

| Size Bucket | Contracts | Total Earned | Total Original | Avg % Complete |
|---|---|---|---|---|
| >$100M | 5 | $767,241,971 | $806,905,704 | 89% |
| $50-100M | 8 | $655,969,538 | $564,543,740 | 96% |
| $10-50M | 21 | $582,590,190 | $550,035,009 | 92% |
| $1-10M | 46 | $177,615,027 | $188,923,434 | 76% |
| <$1M | 15 | $9,184,264 | $9,869,519 | 76% |

> The mega-projects (>$50M) are mostly near completion (89-96%). The smaller contracts ($1-10M and under) at 76% average completion after 3-7 years are the most concerning — these should have been completed long ago.

---

## Biggest Non-FINAL Overruns (2019-2022)

| Contract | Contractor | Original Bid | Total Earned | Overrun $ | Overrun % | % Complete | Days Charged/Allowed | Extra Work |
|---|---|---|---|---|---|---|---|---|
| 09-213404 | FISHER SAND & GRAVEL CO | $69.7M | $96.3M | $26.7M | +38.2% | 94% | 878/500 | $12.4M |
| 07-210624 | OHL USA, INC. | $85.9M | $110.3M | $24.4M | +28.4% | 96% | 992/970 | $7.9M |
| 04-4G0804 | O.C. JONES & SONS, INC. | $143.4M | $160.2M | $16.9M | +11.8% | 99% | 889/940 | $15.7M |
| 05-344904 | A. TEICHERT & SON, INC. | $70.6M | $85.7M | $15.1M | +21.4% | 99% | 490/480 | $20.6M |
| 03-3F0604 | GOLDEN STATE BRIDGE, INC. | $70.8M | $83.3M | $12.5M | +17.7% | 98% | 377/430 | $9.6M |
| 07-307104 | C. A. RASMUSSEN, INC. | $22.7M | $34.4M | $11.7M | +51.6% | 60% | 855/1250 | $14.2M |
| 04-264724 | GHILOTTI CONSTRUCTION | $78.9M | $88.4M | $9.5M | +12.1% | 95% | 703/1000 | $15.6M |
| 04-297634 | BAY CITIES PAVING & GRADING | $133.8M | $142.7M | $8.9M | +6.7% | 98% | 733/1000 | $12.4M |
| 04-0A7724 | O.C. JONES & SONS, INC. | $25.2M | $33.6M | $8.4M | +33.3% | 97% | 596/600 | $9.0M |
| 06-360244 | SECURITY PAVING CO. | $48.9M | $56.3M | $7.4M | +15.2% | 100% | 797/415 | $3.1M |
| 07-327304 | SHIMMICK CONSTRUCTION | $12.2M | $18.5M | $6.3M | +51.3% | 94% | 759/590 | $6.4M |
| 07-291404 | STACY AND WITBECK, INC. | $10.8M | $16.8M | $6.0M | +55.7% | 96% | 793/1515 | $4.7M |
| 12-0P94U4 | GRANITE CONSTRUCTION | $6.8M | $12.0M | $5.2M | +75.5% | 88% | 708/1800 | $8.3M |
| 07-324904 | STACY AND WITBECK, INC. | $4.8M | $9.7M | $4.9M | +102.5% | 100% | 135/135 | $1.7M |

---

## Key Findings

### 1. These Are Not Just Slow — Many Are Dramatically Over Budget

- **07-324904** (Stacy and Witbeck): Original $4.8M, earned $9.7M = **102.5% overrun**. Listed as 100% complete but never reached FINAL.
- **12-0P94U4** (Granite Construction): Original $6.8M, earned $12.0M = **75.5% overrun** with $8.3M in extra work — more extra work than the original contract.
- **09-213404** (Fisher Sand & Gravel): Original $69.7M, earned $96.3M = **$26.7M overrun** with 878 days charged vs 500 allowed (75.6% over time).

### 2. Mega-Projects Dominate the Dollar Exposure

The 5 contracts over $100M account for $767M in earnings. These are major highway reconstruction projects in Bay Area (04-297634, 04-4G0804, 04-264724) and inland areas (09-213404, 07-210624).

### 3. Extra Work Is a Major Cost Driver

Across the top 15 overruns, extra work averages **$11.1M per contract** — often exceeding the overrun itself. This suggests scope changes, not just execution problems.

- 05-344904: $20.6M in extra work on a $70.6M contract (29% of original)
- 04-4G0804: $15.7M in extra work on a $143.4M contract
- 07-307104: $14.2M in extra work, only 60% complete, 51.6% over budget

### 4. The "100% Complete but Not FINAL" Pattern

Several contracts show 100% completion but remain in PROGRESS status:
- **03-1H2404**: 100% complete as of Jan 2026, still PROGRESS
- **01-0E0904**: 100% complete, still PROGRESS
- **07-324904**: 100% complete, AFTER ACCEPTANCE, never finalized

These may be waiting for final accounting, dispute resolution, or the new "RERUN PROGRESS ESTIMATE" status (discovered on PETS portal but not yet in our parsed data).

### 5. Monthly Payment Patterns Reveal Ongoing Activity

Example: **03-1H2404** (Lamon Construction, $5.2M original):
- Started Dec 2022, still in progress Jan 2026 (3+ years)
- Jumped from 82% to 100% between Nov 2025 and Jan 2026
- Total earned: $7.49M (44% over original budget)
- 31 pay estimates over 3 years for a $5.2M contract

Example: **04-297634** (Bay Cities Paving, $133.8M original):
- Started May 2021, 63 estimates over 4.75 years
- Steady monthly payments of $1-3M continuing through Feb 2026
- Currently 98% complete at $142.7M earned

Example: **03-3F0604** (Golden State Bridge, $70.8M original):
- Started Mar 2022, 50 estimates over 4 years
- Monthly payments of $1-2M still active
- Currently 98% complete at $83.3M earned

---

## New Status Type Discovered: "RERUN PROGRESS ESTIMATE"

The PETS portal shows a status type not in our current data: **RERUN PROGRESS ESTIMATE**. This suggests Caltrans can revert a contract's progress and reissue estimates — possibly for rework, corrections, or scope changes.

**Parser update needed:** The `Caltrans_Pay_Estimate_Parser.py` needs to recognize and handle this new status type.

---

## Query: Full Non-FINAL Contract List (2019-2024)

```sql
SELECT
    bs.contract_number,
    bs.district,
    bs.location,
    bs.bid_opening_date,
    toYear(parseDateTimeBestEffort(bs.bid_opening_date)) AS year,
    bs.bid_amount,
    bs.number_of_bids,
    bs.number_of_items,
    latest.current_status,
    latest.max_est AS estimate_no,
    latest.percent_complete,
    latest.contractor_name
FROM (
    SELECT
        contract_number,
        any(district) AS district,
        any(location) AS location,
        any(bid_opening_date) AS bid_opening_date,
        any(bid_amount) AS bid_amount,
        any(number_of_bids) AS number_of_bids,
        any(number_of_items) AS number_of_items
    FROM Caltrans.bid_summary
    WHERE bid_rank = 1
    GROUP BY contract_number
) bs
INNER JOIN (
    SELECT
        contract_number,
        multiIf(
            max(project_status = 'AFTER ACCEPTANCE') = 1, 'AFTER ACCEPTANCE',
            'PROGRESS'
        ) AS current_status,
        max(estimate_no) AS max_est,
        argMax(percent_complete, estimate_no) AS percent_complete,
        argMax(contractor_name, estimate_no) AS contractor_name
    FROM Caltrans.pay_estimates
    GROUP BY contract_number
) latest ON bs.contract_number = latest.contract_number
WHERE bs.contract_number NOT IN (
    SELECT DISTINCT contract_number FROM Caltrans.pay_estimates WHERE project_status = 'FINAL'
)
AND toYear(parseDateTimeBestEffort(bs.bid_opening_date)) <= 2024
ORDER BY year, bs.contract_number
```

---

## Query: Non-FINAL Budget Overrun Summary

```sql
WITH nonfinal AS (
    SELECT pe.contract_number,
        argMax(pe.original_contract_amount, pe.estimate_no) AS original_amt,
        argMax(pe.total_earned, pe.estimate_no) AS earned,
        toFloat64OrZero(argMax(pe.percent_complete, pe.estimate_no)) AS pct_complete,
        argMax(pe.contractor_name, pe.estimate_no) AS contractor,
        argMax(pe.working_days_charged, pe.estimate_no) AS days_charged,
        argMax(pe.contract_days, pe.estimate_no) AS days_allowed,
        argMax(pe.extra_work, pe.estimate_no) AS extra_work
    FROM Caltrans.pay_estimates pe
    WHERE pe.contract_number NOT IN (
        SELECT DISTINCT contract_number FROM Caltrans.pay_estimates WHERE project_status = 'FINAL'
    )
    GROUP BY pe.contract_number
)
SELECT count() AS contracts,
    round(avg(original_amt),0) AS avg_original,
    round(avg(earned),0) AS avg_earned,
    round(avg((earned - original_amt)/original_amt * 100),1) AS avg_overrun_pct,
    round(median((earned - original_amt)/original_amt * 100),1) AS med_overrun_pct,
    round(sum(earned - original_amt),0) AS total_overrun,
    round(avg(toFloat64OrZero(days_charged)),0) AS avg_days_charged,
    round(avg(toFloat64OrZero(days_allowed)),0) AS avg_days_allowed
FROM nonfinal nf
INNER JOIN (
    SELECT contract_number FROM (
        SELECT contract_number, any(bid_opening_date) AS bod
        FROM Caltrans.bid_summary WHERE bid_rank = 1
        GROUP BY contract_number
    ) WHERE toYear(parseDateTimeBestEffort(bod)) BETWEEN 2019 AND 2022
) bs ON nf.contract_number = bs.contract_number
WHERE nf.original_amt > 0
```

---

## Next Steps

1. **Update parser** to handle "RERUN PROGRESS ESTIMATE" status
2. **Re-scrape** the 95 stale contracts to get latest data (some may have finalized since our last scrape)
3. **Investigate** the 15 contracts under $1M that are 3-7 years old at only 76% completion — these are the most anomalous
4. **Track monthly payment velocity** to identify which contracts are still actively spending vs stalled
5. **Cross-reference** with contract days allowed to identify truly delayed vs. legitimately long-duration projects
