# CDOT vs Caltrans Comparison

Data for a follow-up article comparing California (Caltrans) and Colorado (CDOT) DOT contract performance.

## Side-by-Side Metrics

Using the **same methodology**: final cost vs. winning bid (FINAL pay estimates only).

| Metric | Caltrans (CA) | CDOT (CO) | Notes |
|---|---|---|---|
| **Time Period** | 2019-2026 (~7 years) | 2014-2024 (10 years) | |
| **Total Contracts** | 2,292 | 1,173 | CA does ~2x more per year |
| **Total Awarded** | $19.25B | $7.18B | CA is 2.7x larger |
| **Avg Contract** | $8.4M | $6.1M | CA 38% higher per contract |
| **FINAL Contracts** | 1,645 | 1,104 | |
| **Avg Bidders** | 5.2 | 3.5 | CA far more competitive |
| **Sole-Bidder Rate** | 1.8% | 13% | CA's market is 7x less concentrated |
| **Highly Competitive (5+)** | 56.7% | 27% | |
| **Avg Overrun (FINAL)** | +13.0% | +1.2% | Both skewed by outliers; use median |
| **Median Overrun** | +2.7% | +0.7% | Both run over budget; CA more so |
| **Over Budget %** | 67.2% | 53.9% | Both over 50%; CA higher |
| **Under Budget %** | 32.8% | 46.1% | |
| **Total Net Overrun $** | +$496M | +$106M | Both in same direction |
| **Top Contractor** | Granite ($1.69B) | Flatiron ($1.04B) | |
| **Bid vs Engineer Est** | 92.0% (median) | ~95% | Both come in under estimate |
| **Bid Spread (1st-2nd)** | 6.2% median | ~8% | CA tighter due to more bidders |

> **Methodology note:** Previous values for CDOT (median -1.9%, 60.6% under budget) used an incorrect methodology and have been superseded. The correct values above use `award_project_amt` vs `current_project_amt` from `CDOT.v_cpe_contract_final`, matching the Caltrans `original_contract_amount` vs `total_earned` approach. See Q35 in Caltrans_Article_Statistic_Queries.md.

## Key Themes for Article

1. **Both systems go over budget** — CA at 67% over / +2.7% median, CO at 54% over / +0.7% median. Not as different as the old comparison suggested.

2. **Extra work explains most of the CA-CO gap** — CA contracts WITHOUT extra work finish 42.9% over budget at median -0.7% — comparable to CDOT. CA's premium comes from extra work (82.6% of contracts carry some).

3. **CA is more competitive, but over budget more** — 5.2 avg bidders vs 3.5, yet CA still runs more over budget. Competition lowers bid prices but doesn't prevent post-award change orders.

4. **Sole-bidder problem is a CO issue, not CA** — 13% of CO contracts have a single bidder vs only 1.8% in CA.

5. **Scale differences** — CA does ~330 contracts/year vs CO's ~117/year, at 38% higher avg value. CA's infrastructure is simply massive.

6. **Non-FINAL contract backlog** — CA has ongoing contracts from 2023-2025 still in progress. The FINAL overrun numbers will shift as these close out.
