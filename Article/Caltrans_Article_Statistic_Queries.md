# Caltrans Article Statistic Queries

Every statistic in `Caltrans_Article_Final.md` is backed by a query below. Referenced inline as (Q1), (Q2), etc.

**Database:** ClickHouse at `192.168.50.100:8123`, database `Caltrans`

**Key schema notes:**
- `bid_summary` has one row per bidder per contract. `bid_rank = 1` is the low bidder (winner).
- **DEDUPLICATION REQUIRED:** `bid_summary` contains 733 duplicate rows (same contract parsed from multiple source PDFs). All queries touching `bid_summary` must use `GROUP BY contract_number` with `any()` aggregation.
- **DEDUPLICATION REQUIRED:** `bid_items` contains 408,485 duplicate rows (38.4%). Queries touching `bid_items` must use `GROUP BY contract_number, item_no` with `any()` aggregation.
- `pay_estimates` has one row per estimate per contract. `project_status` is FINAL, PROGRESS, or AFTER ACCEPTANCE.
- **SEMI-FINAL status:** Some estimates are labeled "SEMI-FINAL" in source files. These are an intermediate step before FINAL and should be treated as AFTER ACCEPTANCE. The parser was updated to handle this correctly — prior data may have SEMI-FINAL misclassified as FINAL.
- Overrun is calculated as `total_earned` vs `original_contract_amount` (the `current_contract_amount` field equals `original_contract_amount` in FINAL records, so it cannot be used for overrun analysis).
- Caltrans has 12 districts (01-12) instead of CDOT's 5 regions.
- District mapping: 01=Eureka, 02=Redding, 03=Marysville, 04=Oakland/Bay Area, 05=San Luis Obispo, 06=Fresno, 07=Los Angeles, 08=San Bernardino, 09=Bishop, 10=Stockton, 11=San Diego, 12=Irvine/Orange County

**Standard deduplication CTEs:**
```sql
-- bid_summary dedup (use for all bid_summary queries)
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(district) AS district,
        any(bid_opening_date) AS bid_opening_date, any(number_of_bids) AS number_of_bids,
        any(bidder_name) AS bidder_name, any(engineer_estimate) AS engineer_estimate,
        any(location) AS location, any(number_of_items) AS number_of_items
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)

-- bid_items dedup (use for all bid_items queries)
WITH bi AS (
    SELECT contract_number, item_no, any(item_code) AS item_code,
        any(item_description) AS descr, any(unit) AS unit,
        any(unit_price) AS unit_price, any(bid_amount) AS amt
    FROM Caltrans.bid_items WHERE bidder_type = 'LOW_BIDDER'
    GROUP BY contract_number, item_no
)
```

---

## Q1: Total contracts, total value, avg contract

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT count() AS total_contracts,
    round(sum(bid_amount) / 1000000000, 2) AS total_value_billions,
    round(avg(bid_amount) / 1000000, 1) AS avg_contract_millions,
    round(max(bid_amount), 0) AS largest_contract,
    round(min(bid_amount), 0) AS smallest_contract
FROM bs
```

| total_contracts | total_value_billions | avg_contract_millions | largest_contract | smallest_contract |
|---|---|---|---|---|
| 2,292 | 19.25 | 8.4 | $274,852,000 | $64,350 |

---

## Q2: Completed contracts (FINAL pay estimates only)

```sql
SELECT count(DISTINCT pe.contract_number) AS completed
FROM Caltrans.pay_estimates pe
WHERE pe.project_status = 'FINAL'
  AND pe.contract_number IN (
    SELECT contract_number FROM Caltrans.bid_summary WHERE bid_rank = 1 GROUP BY contract_number
  )
```

| completed |
|---|
| 1,619 |

---

## Q2b: Project status breakdown (all statuses — not mutually exclusive)

```sql
SELECT
  project_status,
  count(DISTINCT contract_number) AS contracts
FROM Caltrans.pay_estimates
GROUP BY project_status
ORDER BY contracts DESC
```

| project_status | contracts |
|---|---|
| PROGRESS | 2,084 |
| AFTER ACCEPTANCE | 1,690 |
| FINAL | 1,644 |

> Note: These counts overlap — a single contract passes through PROGRESS -> AFTER ACCEPTANCE -> FINAL. See Q3 for mutually exclusive waterfall.

---

## Q3: Annual contract summary (waterfall: FINAL > non-FINAL with PE > no PE)

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(bid_opening_date) AS bid_opening_date,
        any(number_of_bids) AS number_of_bids
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT
  toYear(parseDateTimeBestEffort(bs.bid_opening_date)) AS year,
  count() AS contracts,
  countIf(bs.contract_number IN (
    SELECT DISTINCT contract_number FROM Caltrans.pay_estimates WHERE project_status = 'FINAL'
  )) AS completed,
  countIf(bs.contract_number NOT IN (
    SELECT DISTINCT contract_number FROM Caltrans.pay_estimates WHERE project_status = 'FINAL'
  ) AND bs.contract_number IN (
    SELECT DISTINCT contract_number FROM Caltrans.pay_estimates WHERE project_status IN ('PROGRESS', 'AFTER ACCEPTANCE')
  )) AS in_progress_only,
  countIf(bs.contract_number NOT IN (
    SELECT DISTINCT contract_number FROM Caltrans.pay_estimates
  )) AS no_pay_estimate,
  round(sum(bs.bid_amount), 0) AS total_value,
  round(avg(bs.bid_amount), 0) AS avg_contract,
  round(avg(toUInt32OrZero(bs.number_of_bids)), 1) AS avg_bidders
FROM bs
GROUP BY year
ORDER BY year
```

| Year | Contracts | Completed | In Progress | No PE | Total Value | Avg Contract | Avg Bidders |
|---|---|---|---|---|---|---|---|
| 2019 | 334 | 322 | 2 | 10 | $2,705,389,358 | $8,099,968 | 5.3 |
| 2020 | 305 | 279 | 13 | 13 | $2,036,255,883 | $6,676,249 | 5.9 |
| 2021 | 344 | 307 | 21 | 16 | $2,296,891,674 | $6,677,011 | 5.9 |
| 2022 | 369 | 302 | 59 | 8 | $2,802,265,723 | $7,594,216 | 4.8 |
| 2023 | 334 | 238 | 84 | 12 | $2,823,456,370 | $8,453,462 | 4.4 |
| 2024 | 295 | 131 | 155 | 9 | $2,831,811,356 | $9,599,361 | 5.0 |
| 2025 | 280 | 38 | 129 | 113 | $3,517,181,457 | $12,561,362 | 5.7 |
| 2026 | 29 | 0 | 0 | 29 | $236,187,587 | $8,144,400 | 5.8 |

> Note: 2017-2018 have only 1 contract each (outlier scraping). Core dataset spans 2019-2026. Columns are mutually exclusive and sum to contracts total.

---

## Q4: Top 10 contractors — contracts won, total bids, win rate, total awarded

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(bidder_name) AS bidder_name
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
),
winners AS (
    SELECT bidder_name AS contractor, count() AS contracts_won, round(sum(bid_amount), 0) AS total_awarded
    FROM bs WHERE bidder_name != ''
    GROUP BY bidder_name ORDER BY total_awarded DESC LIMIT 10
),
total_bids AS (
    SELECT bidder_name AS contractor, count(DISTINCT contract_number) AS total_bids
    FROM Caltrans.bid_summary WHERE bidder_name IN (SELECT contractor FROM winners)
    GROUP BY bidder_name
)
SELECT w.contractor, w.contracts_won, t.total_bids,
    round(w.contracts_won * 100.0 / t.total_bids, 1) AS win_rate_pct, w.total_awarded
FROM winners w LEFT JOIN total_bids t ON w.contractor = t.contractor
ORDER BY w.total_awarded DESC
```

| Contractor | Contracts Won | Total Bids | Win Rate % | Total Awarded |
|---|---|---|---|---|
| GRANITE CONSTRUCTION COMPANY | 147 | 585 | 25.1% | $1,685,593,407 |
| SECURITY PAVING COMPANY, INC. | 25 | 166 | 15.1% | $1,111,884,219 |
| BAY CITIES PAVING & GRADING, INC. | 20 | 49 | 40.8% | $677,271,243 |
| O.C. JONES & SONS, INC. | 50 | 114 | 43.9% | $590,077,325 |
| MYERS & SONS CONSTRUCTION, LLC | 59 | 307 | 19.2% | $554,622,191 |
| GRIFFITH COMPANY | 48 | 208 | 23.1% | $496,406,957 |
| BAY CITIES PAVING & GRADING, | 21 | 52 | 40.4% | $468,188,575 |
| GOLDEN STATE BRIDGE, INC. | 22 | 177 | 12.4% | $385,294,373 |
| DESILVA GATES CONSTRUCTION LLC | 5 | 25 | 20.0% | $294,059,772 |
| FLATIRON WEST, INC. | 3 | 30 | 10.0% | $292,926,858 |

> **Data quality note:** "BAY CITIES PAVING & GRADING, INC." and "BAY CITIES PAVING & GRADING," appear as separate entries due to inconsistent naming in source PDFs. Combined they would be 41 wins, ~$1.15B — making them the #2 contractor behind Granite.

---

## Q5: Top 10 combined total and percentage of all spending

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(bidder_name) AS bidder_name
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
),
winners AS (SELECT bidder_name AS contractor, count() AS contracts_won, sum(bid_amount) AS total_awarded
    FROM bs WHERE bidder_name != '' GROUP BY bidder_name),
top10 AS (SELECT contractor, contracts_won, total_awarded FROM winners ORDER BY total_awarded DESC LIMIT 10),
overall AS (SELECT count() AS total_contracts, sum(bid_amount) AS total_dollars FROM bs)
SELECT sum(t.total_awarded) AS top10_dollars, any(o.total_dollars) AS overall_dollars,
    round(sum(t.total_awarded) / any(o.total_dollars) * 100, 1) AS pct_of_total_dollars,
    sum(t.contracts_won) AS top10_contracts, any(o.total_contracts) AS overall_contracts
FROM top10 t CROSS JOIN overall o
```

| top10_dollars | pct_of_total | top10_contracts | overall_contracts |
|---|---|---|---|
| $6,556,324,921 | 34.1% | 400 | 2,292 |

---

## Q6: Contractor detail — avg contract, largest, district focus

(See Q4 for base data. District focus from Q23.)

---

## Q7: Spending by Caltrans district

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(district) AS district,
        any(number_of_bids) AS number_of_bids
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT district,
    multiIf(district='01','Eureka', district='02','Redding', district='03','Marysville',
        district='04','Oakland/Bay Area', district='05','San Luis Obispo', district='06','Fresno',
        district='07','Los Angeles', district='08','San Bernardino', district='09','Bishop',
        district='10','Stockton', district='11','San Diego', district='12','Irvine/Orange County',
        'Unknown') AS district_name,
    count() AS contracts, round(sum(bid_amount),0) AS total_value,
    round(avg(bid_amount),0) AS avg_contract, round(avg(toUInt32OrZero(number_of_bids)),1) AS avg_bidders
FROM bs
GROUP BY district ORDER BY total_value DESC
```

| District | Name | Contracts | Total Value | Avg Contract | Avg Bidders |
|---|---|---|---|---|---|
| 04 | Oakland / Bay Area | 331 | $3,246,940,805 | $9,809,489 | 5.3 |
| 07 | Los Angeles | 300 | $2,601,870,089 | $8,672,900 | 6.1 |
| 08 | San Bernardino | 236 | $2,380,959,261 | $10,088,810 | 6.2 |
| 03 | Marysville | 247 | $2,250,867,459 | $9,112,824 | 5.0 |
| 12 | Irvine / Orange County | 159 | $1,736,285,220 | $10,920,033 | 7.0 |
| 06 | Fresno | 212 | $1,600,797,517 | $7,550,932 | 4.7 |
| 05 | San Luis Obispo | 163 | $1,083,770,882 | $6,648,901 | 4.3 |
| 11 | San Diego | 121 | $1,076,286,232 | $8,894,928 | 5.0 |
| 01 | Eureka | 130 | $1,017,873,378 | $7,829,795 | 4.8 |
| 10 | Stockton | 174 | $974,849,133 | $5,602,581 | 4.9 |
| 02 | Redding | 143 | $803,816,883 | $5,621,097 | 4.3 |
| 09 | Bishop | 76 | $479,611,618 | $6,310,679 | 3.9 |

---

## Q8: Overrun summary — FINAL contracts: total_earned vs original_contract_amount

```sql
SELECT count() AS completed,
    round(avg(overrun_pct), 1) AS avg_overrun,
    round(median(overrun_pct), 1) AS median_overrun,
    round(countIf(overrun_pct < 0) * 100.0 / count(), 1) AS pct_under,
    round(sum(overrun_dollars), 0) AS total_overrun
FROM (
    SELECT pe.contract_number,
        pe.original_contract_amount AS original_bid,
        pe.total_earned AS final_cost,
        (pe.total_earned - pe.original_contract_amount) AS overrun_dollars,
        (pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount * 100 AS overrun_pct
    FROM Caltrans.pay_estimates pe
    WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 0
      AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
          WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
)
```

| completed | avg_overrun | median_overrun | pct_under | total_overrun |
|---|---|---|---|---|
| 1,644 | +13.1% | +2.7% | 33.3% | $579,743,602 |

> **Note:** The high average (+13.1%) is skewed by outliers (see Q11). The median of +2.7% is a more representative measure. One contract (04-0A771) has a 15,214% overrun due to an original_contract_amount of only $6,095 — likely a data entry error.

---

## Q9: Overrun distribution buckets

```sql
WITH overruns AS (
    SELECT (pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount * 100 AS overrun_pct
    FROM Caltrans.pay_estimates pe
    WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 0
      AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
          WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
)
SELECT multiIf(overrun_pct > 50, '> 50% over', overrun_pct > 20, '20-50% over',
    overrun_pct > 5, '5-20% over', overrun_pct >= 0, '0-5% over', 'Under budget') AS range,
    count() AS contracts
FROM overruns GROUP BY range
ORDER BY multiIf(range='> 50% over',1,range='20-50% over',2,range='5-20% over',3,range='0-5% over',4,5)
```

| Overrun Range | Contracts |
|---|---|
| > 50% over budget | 15 |
| 20% to 50% over | 116 |
| 5% to 20% over | 478 |
| 0% to 5% over | 488 |
| Under budget (savings) | 547 |

---

## Q10: Top 5 largest completed projects by final cost

```sql
SELECT pe.contract_number, pe.contractor_name,
    round(pe.original_contract_amount, 0) AS winning_bid,
    round(pe.total_earned, 0) AS final_cost,
    round(pe.total_earned - pe.original_contract_amount, 0) AS overrun_dollars,
    round((pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount * 100, 1) AS overrun_pct
FROM Caltrans.pay_estimates pe
WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 0
  AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
      WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
ORDER BY pe.total_earned DESC LIMIT 5
```

| Contract | Contractor | Winning Bid | Final Cost | Overrun $ | Overrun % |
|---|---|---|---|---|---|
| 03-0H10U4 | NOR CAL PAVING | $274,852,000 | $295,612,990 | $20,760,990 | +7.6% |
| 08-1C0824 | FISHER SAND & GRAVEL CO. | $267,839,839 | $266,555,520 | -$1,284,319 | -0.5% |
| 08-1C38U4 | COFFMAN SPECIALTIES, INC | $181,885,000 | $184,631,760 | $2,746,760 | +1.5% |
| 12-0K0224 | FLATIRON WEST, INC. | $129,773,276 | $151,797,433 | $22,024,157 | +17.0% |
| 08-0K1224 | SULLY-MILLER CONTRACTING | $121,672,000 | $143,921,921 | $22,249,921 | +18.3% |

---

## Q11: Worst overruns by percentage (contracts > $1M)

```sql
SELECT pe.contract_number, pe.contractor_name,
    round(pe.original_contract_amount, 0) AS winning_bid,
    round(pe.total_earned, 0) AS final_cost,
    round(pe.total_earned - pe.original_contract_amount, 0) AS overrun_dollars,
    round((pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount * 100, 1) AS overrun_pct
FROM Caltrans.pay_estimates pe
WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 1000000
  AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
      WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
ORDER BY overrun_pct DESC LIMIT 10
```

| Contract | Contractor | Winning Bid | Final Cost | Overrun $ | Overrun % |
|---|---|---|---|---|---|
| 04-3G4544 | (parsing issue) | $14,858,813 | $44,434,385 | $29,575,572 | +199.0% |
| 11-2N0424 | HAZARD CONSTRUCTION CO. | $1,708,547 | $3,263,146 | $1,554,599 | +91.0% |
| 06-0U4704 | (parsing issue) | $24,198,298 | $43,408,610 | $19,210,313 | +79.4% |
| 04-3G6204 | MYERS AND SONS CONSTRUCTION | $20,349,212 | $35,106,551 | $14,757,339 | +72.5% |
| 04-3G4744 | (parsing issue) | $38,401,065 | $65,655,672 | $27,254,607 | +71.0% |
| 10-1C8004 | CALIFORNIA ENGINEERING | $6,417,007 | $10,690,787 | $4,273,780 | +66.6% |
| 08-0G6914 | SUKUT CONSTRUCTION, LLC | $5,568,899 | $9,152,679 | $3,583,781 | +64.4% |
| 12-0T3204 | DIVERSIFIED LANDSCAPE CO. | $1,813,166 | $2,797,397 | $984,231 | +54.3% |
| 10-1J5204 | (parsing issue) | $2,683,683 | $3,856,525 | $1,172,842 | +43.7% |
| 04-0Y2604 | (parsing issue) | $2,870,731 | $4,116,837 | $1,246,106 | +43.4% |

---

## Q12: Highest average overruns by contractor (min 3 FINAL contracts)

```sql
SELECT pe.contractor_name AS contractor, count() AS contracts,
    round(avg((pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount * 100), 1) AS avg_overrun_pct,
    round(sum(pe.total_earned - pe.original_contract_amount), 0) AS total_overrun_dollars
FROM Caltrans.pay_estimates pe
WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 0
  AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
      WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
GROUP BY pe.contractor_name HAVING contracts >= 3
ORDER BY avg_overrun_pct DESC LIMIT 10
```

| Contractor | Contracts | Avg Overrun % | Total Overrun $ |
|---|---|---|---|
| MARINA LANDSCAPE INC. | 3 | +48.2% | $675,447 |
| SUKUT CONSTRUCTION, LLC | 3 | +23.8% | $4,819,834 |
| DIVERSIFIED LANDSCAPE CO. | 4 | +23.4% | $2,758,402 |
| DIG IT CONSTRUCTION, INC | 3 | +22.2% | $814,821 |
| HAZARD CONSTRUCTION COMPANY | 6 | +17.5% | $2,781,273 |
| SOUZA ENGINEERING CONTRACTING | 5 | +17.2% | $2,622,035 |
| PAL GENERAL ENGINEERING INC. | 3 | +14.6% | $865,360 |
| FEC FUTURE CONTRACTORS AND | 4 | +12.9% | $1,034,220 |
| GHILOTTI CONSTRUCTION CO. | 4 | +12.4% | $15,733,916 |

> Note: GOLDEN STATE BRIDGE, INC. (11 contracts, avg +1,390%) excluded — driven by one outlier contract (04-0A771) with $6,095 original amount.

---

## Q13: Most under budget contractors (min 3 FINAL contracts)

```sql
SELECT pe.contractor_name AS contractor, count() AS contracts,
    round(avg((pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount * 100), 1) AS avg_overrun_pct,
    round(sum(pe.total_earned - pe.original_contract_amount), 0) AS total_savings_dollars
FROM Caltrans.pay_estimates pe
WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 0
  AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
      WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
GROUP BY pe.contractor_name HAVING contracts >= 3
ORDER BY avg_overrun_pct ASC LIMIT 10
```

| Contractor | Contracts | Avg Overrun % | Total Savings $ |
|---|---|---|---|
| HIGHLAND CONSTRUCTION, INC. | 4 | -18.9% | -$1,699,231 |
| POLO ENGINEERING, INC. | 4 | -18.6% | -$988,827 |
| PAL GENERAL ENGINEERING INC | 5 | -18.4% | -$5,328,404 |
| PAPICH CONSTRUCTION CO., INC. | 6 | -16.3% | -$4,183,974 |
| SAN PATRICIO CONSTRUCTION, INC | 3 | -15.7% | -$857,988 |
| TAYLOR JANE CONSTRUCTION LP | 4 | -12.0% | -$257,571 |
| CENTRAL STRIPING SERVICE, INC. | 9 | -11.0% | -$1,269,081 |
| STERNDAHL ENTERPRISES LLC | 4 | -10.8% | -$522,598 |
| T.P.A. CONSTRUCTION, INC. | 4 | -9.3% | -$383,780 |

---

## Q14: Competition metrics by year

```sql
WITH bs AS (
    SELECT contract_number, any(bid_opening_date) AS bid_opening_date,
        any(number_of_bids) AS number_of_bids
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT toYear(parseDateTimeBestEffort(bid_opening_date)) AS year, count() AS contracts,
    round(avg(toUInt32OrZero(number_of_bids)), 1) AS avg_bidders,
    round(countIf(toUInt32OrZero(number_of_bids) = 1) * 100.0 / count(), 1) AS sole_bidder_pct,
    round(countIf(toUInt32OrZero(number_of_bids) >= 5) * 100.0 / count(), 1) AS highly_competitive_pct
FROM bs
GROUP BY year ORDER BY year
```

| Year | Contracts | Avg Bidders | Sole-Bidder % | Highly Competitive (5+) % |
|---|---|---|---|---|
| 2019 | 334 | 5.3 | 2.4% | 59.6% |
| 2020 | 305 | 5.9 | 0.7% | 71.5% |
| 2021 | 344 | 5.9 | 1.5% | 67.2% |
| 2022 | 369 | 4.8 | 1.9% | 50.1% |
| 2023 | 334 | 4.4 | 3.0% | 38.3% |
| 2024 | 295 | 5.0 | 1.4% | 54.6% |
| 2025 | 280 | 5.7 | 1.1% | 66.8% |
| 2026 | 29 | 5.8 | 0.0% | 75.9% |

---

## Q15: Bid vs engineer's estimate

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(engineer_estimate) AS engineer_estimate
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT
    round(median(bid_amount / engineer_estimate) * 100, 1) AS median_bid_vs_estimate_pct,
    round(countIf(bid_amount < engineer_estimate) * 100.0 / count(), 1) AS pct_under_estimate,
    count() AS n
FROM bs
WHERE engineer_estimate > 10000 AND bid_amount > 0
```

| median_bid_vs_estimate | pct_under_estimate | n |
|---|---|---|
| 92.0% | 67.4% | 2,277 |

> **Data quality note:** 15 contracts have engineer_estimate < $10,000 (parsing errors from bid tab PDFs where the value was truncated). These create 1000x+ ratios that make the average meaningless (308% even after filtering). Median of 92.0% is the reliable measure — typical winning bids come in 8% below the engineer's estimate. 67.4% of winning bids are under the estimate.

---

## Q16: Top spending categories (low bidder only)

```sql
WITH bi AS (
    SELECT contract_number, item_no, any(item_description) AS descr, any(bid_amount) AS amt
    FROM Caltrans.bid_items
    WHERE bidder_type = 'LOW_BIDDER' AND bid_amount > 0
    GROUP BY contract_number, item_no
)
SELECT
    multiIf(
        descr LIKE '%MOBILIZATION%' OR descr LIKE '%Mobilization%', 'Mobilization',
        descr LIKE '%HOT MIX ASPHALT%' OR descr LIKE '%HMA%', 'Hot Mix Asphalt',
        descr LIKE '%ROADWAY EXCAVATION%', 'Roadway Excavation',
        descr LIKE '%STRUCTURAL CONCRETE%', 'Structural Concrete',
        descr LIKE '%AGGREGATE BASE%', 'Aggregate Base',
        descr LIKE '%REINFORCING STEEL%', 'Reinforcing Steel',
        descr LIKE '%CONSTRUCTION AREA SIGN%', 'Construction Area Signs',
        descr LIKE '%TRAFFIC CONTROL%', 'Traffic Control System',
        descr LIKE '%CONCRETE BARRIER%', 'Concrete Barrier',
        descr LIKE '%CLEARING AND GRUBBING%' OR descr LIKE '%CLEAR AND GRUB%', 'Clearing & Grubbing',
        'Other'
    ) AS category,
    count(DISTINCT contract_number) AS contracts,
    round(sum(amt), 0) AS total_spent
FROM bi
GROUP BY category HAVING category != 'Other'
ORDER BY total_spent DESC LIMIT 10
```

| Category | Contracts | Total Spent |
|---|---|---|
| Hot Mix Asphalt | 1,637 | $2,834,068,721 |
| Mobilization | 1,780 | $1,564,842,769 |
| Structural Concrete | 940 | $929,028,010 |
| Traffic Control System | 2,251 | $846,863,966 |
| Roadway Excavation | 1,067 | $629,139,887 |
| Concrete Barrier | 600 | $465,070,064 |
| Aggregate Base | 950 | $292,908,817 |
| Reinforcing Steel | 532 | $183,680,873 |
| Clearing & Grubbing | 1,019 | $97,252,059 |
| Construction Area Signs | 2,191 | $68,347,446 |

> Note: bid_items required deduplication (408,485 duplicate rows, 38.4%). Previous values were inflated 40-60%. These corrected totals use `GROUP BY contract_number, item_no` with `any()` aggregation.

---

## Q17: Most worked routes

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(location) AS location
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT multiIf(
    location LIKE '%-5-%' OR location LIKE '%-05-%', 'I-5',
    location LIKE '%-10-%' OR location LIKE '%-010-%', 'I-10',
    location LIKE '%-15-%' OR location LIKE '%-015-%', 'I-15',
    location LIKE '%-80-%' OR location LIKE '%-080-%', 'I-80',
    location LIKE '%-101-%', 'US-101',
    location LIKE '%-405-%', 'I-405',
    location LIKE '%-210-%', 'I-210',
    location LIKE '%-99-%' OR location LIKE '%-099-%', 'SR-99',
    location LIKE '%-680-%', 'I-680',
    location LIKE '%-40-%' OR location LIKE '%-040-%', 'I-40',
    'Other') AS highway,
    count() AS contracts,
    round(sum(bid_amount), 0) AS total_bid_value
FROM bs
GROUP BY highway HAVING highway != 'Other'
ORDER BY total_bid_value DESC LIMIT 10
```

| Highway | Contracts | Total Bid Value |
|---|---|---|
| I-5 | 169 | $2,002,901,744 |
| US-101 | 149 | $1,602,065,359 |
| SR-99 | 81 | $947,467,494 |
| I-80 | 59 | $856,916,643 |
| I-10 | 41 | $783,377,284 |
| I-15 | 44 | $453,258,606 |
| I-405 | 24 | $331,086,494 |
| I-680 | 14 | $302,503,647 |
| I-210 | 33 | $224,210,380 |
| I-40 | 13 | $156,993,631 |

---

## Q18: Missing pay estimate breakdown by year

```sql
WITH bs AS (
    SELECT contract_number, any(bid_opening_date) AS bid_opening_date
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT toYear(parseDateTimeBestEffort(bs.bid_opening_date)) AS year, count() AS total,
    countIf(bs.contract_number IN (SELECT DISTINCT contract_number FROM Caltrans.pay_estimates WHERE project_status = 'FINAL')) AS has_final,
    countIf(bs.contract_number NOT IN (SELECT DISTINCT contract_number FROM Caltrans.pay_estimates WHERE project_status = 'FINAL')
        AND bs.contract_number IN (SELECT DISTINCT contract_number FROM Caltrans.pay_estimates
        WHERE project_status IN ('PROGRESS','AFTER ACCEPTANCE'))) AS in_progress,
    countIf(bs.contract_number NOT IN (SELECT DISTINCT contract_number FROM Caltrans.pay_estimates)) AS no_pe
FROM bs
WHERE toYear(parseDateTimeBestEffort(bs.bid_opening_date)) BETWEEN 2019 AND 2024
GROUP BY year ORDER BY year
```

| Year | Total Contracts | Has Final | In Progress | No Pay Estimate |
|---|---|---|---|---|
| 2019 | 334 | 322 | 2 | 10 |
| 2020 | 305 | 279 | 13 | 13 |
| 2021 | 344 | 307 | 21 | 16 |
| 2022 | 369 | 302 | 59 | 8 |
| 2023 | 334 | 238 | 84 | 12 |
| 2024 | 295 | 131 | 155 | 9 |

---

## Q19: AFTER ACCEPTANCE analysis (Caltrans-specific)

```sql
SELECT project_status, count(DISTINCT contract_number) AS contracts,
    round(avg(current_contract_amount), 0) AS avg_contract_value,
    round(sum(current_contract_amount), 0) AS total_value
FROM Caltrans.pay_estimates pe
WHERE pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
    WHERE pe2.contract_number = pe.contract_number)
GROUP BY project_status ORDER BY total_value DESC
```

| Status | Contracts | Avg Contract Value | Total Value |
|---|---|---|---|
| FINAL | 1,643 | $5,171,797 | $8,497,262,892 |
| PROGRESS | 394 | $17,724,161 | $7,160,561,065 |
| AFTER ACCEPTANCE | 78 | $7,825,021 | $610,351,648 |

---

## Q20: Payment history analysis — total disbursed by type

```sql
SELECT type, project_status, count() AS payments, count(DISTINCT contract_number) AS contracts,
    round(sum(disbursed), 0) AS total_disbursed, round(sum(held), 0) AS total_held
FROM Caltrans.payment_history GROUP BY type, project_status ORDER BY total_disbursed DESC
```

| Type | Status | Payments | Contracts | Total Disbursed | Total Held |
|---|---|---|---|---|---|
| P/P | PROGRESS | 23,243 | 2,093 | $14,112,226,810 | $99,423,976 |
| A/A | AFTER ACCEPTANCE | 1,969 | 1,731 | $200,408,055 | $3,841,359 |
| (blank) | PROGRESS | 1,501 | 893 | $126,613,099 | $7,080,564 |
| FIN | FINAL | 1,735 | 1,611 | $39,967,208 | $585,132 |

---

## Q21: Schedule analysis — working days charged vs allowed (FINAL only)

```sql
SELECT round(avg(toFloat64OrZero(working_days_charged)), 0) AS avg_days_charged,
    round(avg(toFloat64OrZero(contract_days)), 0) AS avg_days_allowed,
    round(avg(toFloat64OrZero(weather_days)), 0) AS avg_weather_days,
    round(avg(toFloat64OrZero(cco_days)), 0) AS avg_cco_days,
    round(countIf(toFloat64OrZero(working_days_charged) > toFloat64OrZero(contract_days)) * 100.0 / count(), 1) AS pct_over_time
FROM Caltrans.pay_estimates pe
WHERE pe.project_status = 'FINAL' AND toFloat64OrZero(contract_days) > 0
  AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
      WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
```

| Avg Days Charged | Avg Days Allowed | Avg Weather Days | Avg CCO Days | % Over Time |
|---|---|---|---|---|
| 140 | 145 | 117 | 8 | 22.1% |

---

## Q22: Extra work and CCO (change order) impact

```sql
SELECT count() AS contracts_with_extra_work,
    round(avg(extra_work), 0) AS avg_extra_work,
    round(sum(extra_work), 0) AS total_extra_work,
    round(avg(extra_work / original_contract_amount * 100), 1) AS avg_extra_work_pct,
    round(avg(toFloat64OrZero(cco_days)), 0) AS avg_cco_days
FROM Caltrans.pay_estimates pe
WHERE pe.project_status = 'FINAL' AND pe.extra_work > 0 AND pe.original_contract_amount > 0
  AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
      WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
```

| Contracts w/ Extra Work | Avg Extra Work $ | Total Extra Work $ | Avg Extra Work % | Avg CCO Days |
|---|---|---|---|---|
| 1,359 | $528,972 | $718,872,428 | 18.7% | 10 |

---

## Q22b: Extra work attribution — what share of overruns is extra work vs base item changes?

Filters to over-budget contracts only. Compares gross extra work added vs net movement in base contract items.

```sql
SELECT
    count() AS contracts,
    round(sum(total_earned - original_contract_amount) / 1e6, 1) AS net_overrun_M,
    round(sum(extra_work) / 1e6, 1) AS gross_extra_work_M,
    round((sum(total_earned - original_contract_amount) - sum(extra_work)) / 1e6, 1) AS base_item_delta_M,
    round(sum(extra_work) / sum(total_earned - original_contract_amount) * 100, 1) AS extra_work_pct_of_overrun
FROM Caltrans.pay_estimates pe
WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 0
  AND (pe.total_earned - pe.original_contract_amount) > 0
  AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
      WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
```

| Contracts | Net Overrun $M | Gross Extra Work $M | Base Item Delta $M | Extra Work % of Overrun |
|---|---|---|---|---|
| 1,103 | $607.7M | $615.4M | -$7.8M | 101.3% |

> On contracts that went over budget, extra work accounts for 101% of net cost growth. Base contract items (original scope) came in $7.8M *under* their authorized amounts in aggregate — quantity adjustments and savings on base items almost exactly offset each other. Every dollar of overrun traces to scope added after award.

---

## Q22c: Overrun rate by extra work threshold

```sql
SELECT
    multiIf(ew_pct = 0,        'No extra work',
            ew_pct < 0.05,     'Under 5%',
            ew_pct < 0.10,     '5-10%',
            ew_pct < 0.20,     '10-20%',
            ew_pct < 0.50,     '20-50%',
                               '50%+') AS bucket,
    count() AS contracts,
    round(avg(overrun_pct) * 100, 1) AS avg_overrun_pct,
    round(countIf(overrun_pct > 0) * 100.0 / count(), 1) AS pct_over_budget,
    round(avg(toFloat64OrZero(cco_days)), 1) AS avg_additional_days
FROM (
    SELECT
        (pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount AS overrun_pct,
        pe.extra_work / pe.original_contract_amount AS ew_pct,
        pe.cco_days
    FROM Caltrans.pay_estimates pe
    WHERE pe.project_status = 'FINAL'
      AND pe.original_contract_amount >= 100000
      AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
          WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
)
GROUP BY bucket ORDER BY min(ew_pct)
```

| Extra Work as % of Contract | Contracts | Avg Cost Overrun | % Over Budget | Avg Additional Days |
|---|---|---|---|---|
| No extra work | 287 | -2.7% | 43.2% | 0.4 |
| Under 5% | 775 | +0.2% | 59.0% | 4.8 |
| 5–10% | 301 | +5.8% | 85.4% | 10.7 |
| 10–20% | 179 | +12.9% | 94.4% | 18.7 |
| 20–50% | 88 | +22.4% | 90.9% | 23.0 |
| 50%+ | 15 | +55.6% | 100.0% | 77.2 |

> Contracts under $100K excluded to remove data entry outliers (04-0A771 had a $6,095 original amount producing a 15,214% computed overrun).
> Once extra work exceeds 10%, 94%+ of projects go over budget. The 50%+ bucket (15 contracts) hits 100% over budget with a +55.6% avg overrun and 77 extra days on average.

---

## Q22d: Extra work and overrun rates by contract size

```sql
SELECT
    multiIf(original_contract_amount >= 25e6, 'Over 25M',
            original_contract_amount >= 10e6, '10-25M',
            original_contract_amount >= 5e6,  '5-10M',
            original_contract_amount >= 1e6,  '1-5M',
                                              'Under 1M') AS bucket,
    count() AS contracts,
    round(countIf(extra_work > 0) * 100.0 / count(), 1) AS pct_with_ew,
    round(countIf(overrun_pct > 0) * 100.0 / count(), 1) AS pct_over_budget,
    round(median(overrun_pct) * 100, 1) AS median_overrun_pct
FROM (
    SELECT pe.original_contract_amount, pe.extra_work,
        (pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount AS overrun_pct
    FROM Caltrans.pay_estimates pe
    WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 0
      AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
          WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
)
GROUP BY bucket ORDER BY min(original_contract_amount) ASC
```

| Contract Size | Contracts | Has Extra Work | % Over Budget | Median Overrun |
|---|---|---|---|---|
| Under 1M | 384 | 68.2% | 64.1% | +2.5% |
| 1–5M | 919 | 82.8% | 64.4% | +2.1% |
| 5–10M | 187 | 95.7% | 71.7% | +3.4% |
| 10–25M | 114 | 99.1% | 80.7% | +5.9% |
| Over 25M | 44 | 100.0% | 88.6% | +6.3% |

> Every contract over $25M had extra work added (100%). Extra work prevalence and overrun rates both decline monotonically with contract size, consistent with larger projects having more complex scope that generates change orders.

---

## Q23: Top contractor per district

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(district) AS district,
        any(bidder_name) AS bidder_name
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT district,
    multiIf(district='01','Eureka', district='02','Redding', district='03','Marysville',
        district='04','Oakland/Bay Area', district='05','San Luis Obispo', district='06','Fresno',
        district='07','Los Angeles', district='08','San Bernardino', district='09','Bishop',
        district='10','Stockton', district='11','San Diego', district='12','Irvine/Orange County',
        'Unknown') AS district_name,
    bidder_name AS top_contractor, count() AS contracts_won,
    round(sum(bid_amount), 0) AS total_awarded
FROM bs
GROUP BY district, bidder_name ORDER BY district, total_awarded DESC
LIMIT 1 BY district
```

| District | Name | Top Contractor | Contracts Won | Total Awarded |
|---|---|---|---|---|
| 01 | Eureka | GRANITE CONSTRUCTION COMPANY | 22 | $252,742,313 |
| 02 | Redding | HAT CREEK CONSTRUCTION & MATERIALS, INC. | 13 | $126,098,238 |
| 03 | Marysville | DESILVA GATES CONSTRUCTION LLC | 4 | $290,401,114 |
| 04 | Oakland / Bay Area | BAY CITIES PAVING & GRADING, INC. | 14 | $540,868,363 |
| 05 | San Luis Obispo | GRANITE CONSTRUCTION COMPANY | 23 | $274,545,009 |
| 06 | Fresno | GRANITE CONSTRUCTION COMPANY | 48 | $397,487,984 |
| 07 | Los Angeles | SECURITY PAVING COMPANY, INC. | 6 | $284,002,497 |
| 08 | San Bernardino | GRANITE CONSTRUCTION COMPANY | 17 | $362,753,024 |
| 09 | Bishop | ROAD AND HIGHWAY BUILDERS, LLC | 2 | $75,666,665 |
| 10 | Stockton | BAY CITIES PAVING & GRADING, INC. | 4 | $121,180,648 |
| 11 | San Diego | SKANSKA USA CIVIL WEST | 2 | $114,833,126 |
| 12 | Irvine / Orange County | SECURITY PAVING COMPANY, INC. | 5 | $367,987,886 |

---

## Q24: Top bid items by dollar volume (low bidder)

```sql
WITH bi AS (
    SELECT contract_number, item_no, any(item_code) AS item_code,
        any(item_description) AS descr, any(unit) AS unit,
        any(unit_price) AS unit_price, any(bid_amount) AS amt
    FROM Caltrans.bid_items
    WHERE bidder_type = 'LOW_BIDDER' AND bid_amount > 0 AND unit_price > 0
    GROUP BY contract_number, item_no
)
SELECT item_code, any(descr) AS description, any(unit) AS u,
    count(DISTINCT contract_number) AS contracts, round(avg(unit_price), 2) AS avg_price,
    round(sum(amt), 0) AS total
FROM bi
GROUP BY item_code HAVING contracts >= 10 ORDER BY total DESC LIMIT 15
```

| Item Code | Description | Unit | Contracts | Avg Unit Price | Total Spent |
|---|---|---|---|---|---|
| 999990 | MOBILIZATION | LS | 1,773 | $867,299 | $1,538,587,812 |
| 390132 | HOT MIX ASPHALT (TYPE A) | TON | 1,455 | $439 | $1,434,753,339 |
| 390137 | RUBBERIZED HMA (GAP GRADED) | TON | 522 | $240 | $1,021,903,918 |
| 120100 | TRAFFIC CONTROL SYSTEM | LS | 2,252 | $370,301 | $833,917,865 |
| 090100 | TIME-RELATED OVERHEAD (WDAY) | WDAY | 1,668 | $1,764 | $626,120,143 |
| 190101 | ROADWAY EXCAVATION | CY | 976 | $192 | $549,806,589 |
| 401050 | JOINTED PLAIN CONCRETE PAVEMENT | CY | 108 | $640 | $372,812,308 |
| 994650 | BUILDING WORK | LS | 95 | $3,537,653 | $336,077,017 |
| 400050 | CONTINUOUSLY REINFORCED CONCRETE | CY | 33 | $488 | $287,924,319 |
| 398200 | COLD PLANE ASPHALT CONCRETE | SQYD | 1,132 | $22 | $265,349,607 |
| 401055 | JOINTED PLAIN CONCRETE PAVEMENT (RSC) | CY | 89 | $857 | $264,191,562 |
| 260203 | CLASS 2 AGGREGATE BASE (CY) | CY | 770 | $219 | $254,978,063 |
| 510053 | (F) STRUCTURAL CONCRETE, BRIDGE | CY | 211 | $3,476 | $253,164,177 |
| 871900 | FIBER OPTIC CABLE SYSTEMS | LS | 67 | $3,084,118 | $206,635,908 |
| 411105 | INDIVIDUAL SLAB REPLACEMENT (RSC) | CY | 116 | $1,324 | $199,166,239 |

> Note: Deduplicated using `GROUP BY contract_number, item_no`. Previous values were inflated ~40% due to 408K duplicate rows.

---

## Q25: Engineer estimate accuracy by year

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amount, any(bid_opening_date) AS bid_opening_date,
        any(engineer_estimate) AS engineer_estimate
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
)
SELECT toYear(parseDateTimeBestEffort(bid_opening_date)) AS year, count() AS contracts,
    round(median((bid_amount - engineer_estimate) / engineer_estimate * 100), 1) AS median_pct_over_estimate,
    round(countIf(bid_amount > engineer_estimate) * 100.0 / count(), 1) AS pct_over
FROM bs WHERE engineer_estimate > 0 AND bid_amount > 0
GROUP BY year ORDER BY year
```

| Year | Contracts | Median % vs Estimate | % Over Estimate |
|---|---|---|---|
| 2019 | 334 | -8.9% | 29.9% |
| 2020 | 305 | -14.5% | 18.7% |
| 2021 | 344 | -11.7% | 22.4% |
| 2022 | 369 | -1.9% | 45.3% |
| 2023 | 334 | +1.2% | 51.8% |
| 2024 | 295 | -4.4% | 37.6% |
| 2025 | 280 | -13.5% | 23.2% |
| 2026 | 29 | -13.1% | 20.7% |

> Note: Averages are excluded due to extreme outliers. Median values are the reliable measure. 2022-2023 saw a spike in bids exceeding estimates — likely an inflation/supply chain effect.

---

## Q26: Mobilization as percentage of contract

```sql
WITH bs AS (
    SELECT contract_number, any(bid_amount) AS bid_amt
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
),
bi AS (
    SELECT contract_number, item_no, any(item_description) AS descr, any(bid_amount) AS amt
    FROM Caltrans.bid_items
    WHERE bidder_type = 'LOW_BIDDER' AND item_description LIKE '%MOBILIZATION%'
    GROUP BY contract_number, item_no
),
mob AS (
    SELECT bi.contract_number, sum(bi.amt) / any(bs.bid_amt) * 100 AS mob_pct
    FROM bi
    INNER JOIN bs ON bi.contract_number = bs.contract_number
    WHERE bs.bid_amt > 0
    GROUP BY bi.contract_number
)
SELECT round(avg(mob_pct), 1), round(median(mob_pct), 1), round(max(mob_pct), 1)
FROM mob
```

| Avg Mobilization % | Median Mobilization % | Max Mobilization % |
|---|---|---|
| 8.0% | 9.0% | 29.4% |

> Note: Deduplicated bid_items. Previous values (10.9% avg, 44.4% max) were inflated by duplicate rows.

---

## Q27: Average number of estimates per contract by latest status

```sql
SELECT latest_status AS project_status,
    round(avg(est_count), 1) AS avg_est, max(est_count) AS max_est, count() AS contracts
FROM (
    SELECT contract_number,
        argMax(project_status, toUInt32(estimate_no)) AS latest_status,
        count() AS est_count
    FROM Caltrans.pay_estimates
    GROUP BY contract_number
)
GROUP BY latest_status
ORDER BY contracts DESC
```

| Status | Avg Estimates | Max Estimates | Contracts |
|---|---|---|---|
| FINAL | 12.6 | 73 | 1,642 |
| PROGRESS | 14.0 | 63 | 394 |
| AFTER ACCEPTANCE | 13.5 | 51 | 77 |

> **Fix:** Previous query used `any(project_status)` which returns a random status per contract. Corrected to use `argMax(project_status, estimate_no)` which returns the status of the latest estimate — the true current state of the contract.

---

## Q28: Payment method breakdown (EFT vs Warrant)

```sql
SELECT pmt_type, count() AS payments, count(DISTINCT contract_number) AS contracts,
    round(sum(disbursed), 0) AS total_disbursed, round(avg(disbursed), 0) AS avg_payment
FROM Caltrans.payment_history WHERE disbursed > 0
GROUP BY pmt_type ORDER BY total_disbursed DESC
```

| Payment Type | Payments | Contracts | Total Disbursed | Avg Payment |
|---|---|---|---|---|
| Warrant | 17,722 | 2,110 | $8,278,363,872 | $467,124 |
| EFT | 8,332 | 706 | $6,188,720,054 | $742,765 |

---

## Q29: Data completeness — row counts

```sql
SELECT 'bid_summary' AS table_name, count() AS rows FROM Caltrans.bid_summary
UNION ALL SELECT 'bid_items', count() FROM Caltrans.bid_items
UNION ALL SELECT 'pay_estimates', count() FROM Caltrans.pay_estimates
UNION ALL SELECT 'pay_estimate_items', count() FROM Caltrans.pay_estimate_items
UNION ALL SELECT 'payment_history', count() FROM Caltrans.payment_history
```

| Table | Rows |
|---|---|
| bid_summary | 15,847 |
| bid_items | 1,063,890 |
| pay_estimates | 27,303 |
| pay_estimate_items | 2,299,213 |
| payment_history | 28,448 |

> Note: bid_summary contains 2,292 unique contracts (733 duplicate rows from multi-source PDF parsing). bid_items has 408,485 duplicates (38.4%) — all queries using bid_items must deduplicate with `GROUP BY contract_number, item_no`.

---

## Q30: Contracts with most estimates (longitudinal tracking)

```sql
SELECT pe.contract_number, any(pe.contractor_name), count() AS num_est,
    any(pe.original_contract_amount), max(pe.total_earned),
    round((max(pe.total_earned) - any(pe.original_contract_amount)) / any(pe.original_contract_amount) * 100, 1),
    min(pe.estimate_date), max(pe.estimate_date)
FROM Caltrans.pay_estimates pe WHERE pe.original_contract_amount > 0
GROUP BY pe.contract_number ORDER BY num_est DESC LIMIT 5
```

| Contract | Contractor | # Estimates | Original | Final Earned | Overrun % | First Est | Last Est |
|---|---|---|---|---|---|---|---|
| 12-0K0214 | ORTIZ ENTERPRISES, INC. | 73 | $107,993,733 | $123,821,919 | +14.7% | 12/22/21 | 01/21/25 |
| 12-0K0224 | FLATIRON WEST, INC. | 69 | $129,773,276 | $151,797,433 | +17.0% | 12/23/19 | 01/21/20 |
| 04-297634 | BAY CITIES PAVING & GRADING | 63 | $133,802,176 | $142,730,965 | +6.7% | 12/20/23 | 01/17/25 |
| 12-0K0234 | GUY F ATKINSON CONSTRUCTION | 61 | $90,405,498 | $118,431,301 | +31.0% | 12/22/21 | 01/15/26 |
| 12-0P42U4 | (location in contractor field) | 60 | $15,999,145 | $21,439,106 | +34.0% | 12/30/25 | 01/20/23 |

---

## Q31: Bid spread analysis — how close are bids?

```sql
WITH bs1 AS (
    SELECT contract_number, any(bid_amount) AS bid_amount
    FROM Caltrans.bid_summary WHERE bid_rank = 1
    GROUP BY contract_number
),
bs2 AS (
    SELECT contract_number, any(bid_amount) AS bid_amount
    FROM Caltrans.bid_summary WHERE bid_rank = 2
    GROUP BY contract_number
),
spreads AS (
    SELECT bs1.contract_number,
        (bs2.bid_amount - bs1.bid_amount) / bs1.bid_amount * 100 AS spread_pct
    FROM bs1 INNER JOIN bs2 ON bs1.contract_number = bs2.contract_number
    WHERE bs1.bid_amount > 0 AND bs2.bid_amount > 0
)
SELECT round(avg(spread_pct), 1) AS avg_spread,
    round(median(spread_pct), 1) AS median_spread,
    round(countIf(spread_pct < 5) * 100.0 / count(), 1) AS pct_within_5pct
FROM spreads
```

| avg_spread | median_spread | pct_within_5pct |
|---|---|---|
| 9.5% | 6.2% | 41.3% |

---

## Q35: CDOT comparison — overrun using same methodology (final cost vs. winning bid)

Uses CDOT.v_cpe_contract_final (FINAL pay estimates), joined to CDOT.fact_contract_lifecycle for letting dates.
`award_project_amt` = original winning bid; `current_project_amt` = final cost paid to contractor.
Filtered to 2014–2024 (the CDOT article dataset period) and contracts > $100K.

```sql
SELECT
    count() AS contracts,
    round(avg((current_project_amt - award_project_amt) / award_project_amt * 100), 1) AS avg_overrun_pct,
    round(median((current_project_amt - award_project_amt) / award_project_amt * 100), 1) AS median_overrun_pct,
    round(countIf(current_project_amt < award_project_amt) * 100.0 / count(), 1) AS pct_under_budget,
    round(countIf(current_project_amt > award_project_amt) * 100.0 / count(), 1) AS pct_over_budget,
    round(sum(current_project_amt - award_project_amt), 0) AS total_overrun
FROM CDOT.v_cpe_contract_final cpe
JOIN CDOT.fact_contract_lifecycle fc ON cpe.contract_id = fc.contract_id
WHERE cpe.award_project_amt > 100000
  AND fc.letting_dt IS NOT NULL
  AND toYear(fc.letting_dt) BETWEEN 2014 AND 2024
  AND fc.winning_bid > 0
```

| contracts | avg_overrun_pct | median_overrun_pct | pct_under_budget | pct_over_budget | total_overrun |
|---|---|---|---|---|---|
| 1,104 | +1.2% | +0.7% | 46.1% | 53.9% | $105,932,319 |

> **Key comparison:** Using the exact same methodology (final cost vs. winning bid, FINAL pay estimates):
> - CDOT (CO, 2014–2024): 53.9% over budget, median **+0.7%**
> - Caltrans (CA, 2019–2026): 67.2% over budget, median **+2.7%**
>
> Caltrans contracts **without extra work** (289 contracts): 42.9% over budget, median **-0.7%** — comparable to CDOT.
> Caltrans contracts **with extra work** (1,359 contracts): 72.0% over budget, median **+3.5%**.
>
> **The gap is extra work**, not baseline construction variance. The CDOT comparison file's earlier values (-1.9% median, 60.6% under budget) used a different/incorrect methodology and have been superseded by this query.

---

## Q36: Extra work vs. no extra work overrun comparison

```sql
SELECT
    has_extra_work,
    count() AS contracts,
    round(median(overrun_pct), 1) AS median_overrun,
    round(countIf(overrun_pct > 0) * 100.0 / count(), 1) AS pct_over_budget,
    round(avg(overrun_pct), 1) AS avg_overrun
FROM (
    SELECT pe.contract_number,
        (pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount * 100 AS overrun_pct,
        pe.extra_work > 0 AS has_extra_work
    FROM Caltrans.pay_estimates pe
    WHERE pe.project_status = 'FINAL' AND pe.original_contract_amount > 0
      AND pe.estimate_no = (SELECT max(pe2.estimate_no) FROM Caltrans.pay_estimates pe2
          WHERE pe2.contract_number = pe.contract_number AND pe2.project_status = 'FINAL')
)
GROUP BY has_extra_work ORDER BY has_extra_work
```

| Has Extra Work | Contracts | Median Overrun | % Over Budget | Avg Overrun |
|---|---|---|---|---|
| No (0) | 289 | -0.7% | 42.9% | -2.7% |
| Yes (1) | 1,359 | +3.5% | 72.0% | +16.3% |

---

## Q22e: Item-level overruns by category (FINAL contracts)

Compares `original_auth_amount` vs `total_est_amount` across `pay_estimate_items` for the latest FINAL estimate per contract.
Excludes force-account items and items with no original authorization.
Groups by item description keyword to surface the top categories by gross overrun dollars.

```sql
WITH final_estimates AS (
    SELECT contract_number, max(estimate_no) AS last_est
    FROM Caltrans.pay_estimates
    WHERE project_status = 'FINAL'
    GROUP BY contract_number
),
items AS (
    SELECT
        pei.contract_number,
        pei.item_description,
        pei.original_auth_amount,
        pei.total_est_amount,
        (pei.total_est_amount - pei.original_auth_amount) AS overrun_dollars
    FROM Caltrans.pay_estimate_items pei
    INNER JOIN final_estimates fe
        ON pei.contract_number = fe.contract_number
        AND pei.estimate_no = fe.last_est
    WHERE pei.original_auth_amount > 0
      AND pei.is_force_account = ''
),
categorized AS (
    SELECT contract_number, item_description,
        original_auth_amount, total_est_amount, overrun_dollars,
        multiIf(
            upper(item_description) LIKE '%HOT MIX ASPHALT%' OR upper(item_description) LIKE '%HMA%', 'Hot Mix Asphalt',
            upper(item_description) LIKE '%ROADWAY EXCAVATION%', 'Roadway Excavation',
            upper(item_description) LIKE '%TIME-RELATED OVERHEAD%' OR upper(item_description) LIKE '%TIME RELATED OVERHEAD%', 'Time-Related Overhead',
            upper(item_description) LIKE '%COLD PLANE%' OR upper(item_description) LIKE '%COLD MILL%', 'Cold Plane AC',
            upper(item_description) LIKE '%AGGREGATE BASE%', 'Aggregate Base',
            NULL
        ) AS category
    FROM items
    WHERE category IS NOT NULL
)
SELECT
    category,
    count(DISTINCT contract_number) AS contracts,
    sumIf(overrun_dollars, overrun_dollars > 0) AS gross_over_M,
    round(avg(total_est_amount / original_auth_amount - 1) * 100, 1) AS avg_overrun_pct
FROM categorized
GROUP BY category
ORDER BY gross_over_M DESC
```

| Item Category | Contracts | Gross Overrun $ | Avg Overrun % |
|---|---|---|---|
| Hot Mix Asphalt | 1,147 | $75.3M | +13.2% |
| Roadway Excavation | 665 | $27.8M | +6.3% |
| Time-Related Overhead | 1,369 | $22.5M | +3.3% |
| Cold Plane AC | 795 | $8.5M | +4.3% |
| Aggregate Base | 585 | $6.0M | +5.4% |

> Note: Hot Mix Asphalt has a large gross overrun ($75.3M) but a net of **-$46.9M** across all contracts. Time-Related Overhead's $22.5M gross overrun reflects accumulated daily overhead charges on delayed projects.

---

## Q34: Contracts without extra work — overrun breakdown

Contracts where `extra_work = 0` in the latest FINAL pay estimate. See Q36 for the full split.

```sql
SELECT
    count() AS contracts,
    round(median(overrun_pct), 1) AS median_overrun,
    round(avg(overrun_pct), 1) AS avg_overrun,
    round(countIf(overrun_pct > 0) * 100.0 / count(), 1) AS pct_over_budget,
    round(countIf(abs(overrun_pct) <= 5) * 100.0 / count(), 1) AS pct_within_5pct
FROM (
    SELECT
        pe.contract_number,
        (pe.total_earned - pe.original_contract_amount) / pe.original_contract_amount * 100 AS overrun_pct
    FROM Caltrans.pay_estimates pe
    WHERE pe.project_status = 'FINAL'
      AND pe.original_contract_amount > 0
      AND pe.extra_work = 0
      AND pe.estimate_no = (
          SELECT max(pe2.estimate_no)
          FROM Caltrans.pay_estimates pe2
          WHERE pe2.contract_number = pe.contract_number
            AND pe2.project_status = 'FINAL'
      )
)
```

| Contracts | Median Overrun | Avg Overrun | % Over Budget | % Within 5% |
|---|---|---|---|---|
| 289 | -0.7% | -2.7% | 42.9% | 67.5% |

> Without post-award scope additions, Caltrans contract execution is comparable to CDOT's baseline: -0.7% median and 67.5% within 5% indicate routine quantity variance, not systematic cost failure.
