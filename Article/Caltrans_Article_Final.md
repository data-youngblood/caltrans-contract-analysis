# Inside California's Highway Machine: Who Builds Caltrans Roads, What It Costs, and Where the Money Goes

California spends more on highway construction than any other state. Caltrans — the California Department of Transportation — oversees thousands of contracts across 12 districts, from the foggy redwood corridors of District 01 (Eureka) to the sprawling freeways of District 07 (Los Angeles) and the desert highways of District 09 (Bishop).

But how efficient is that spending? When Caltrans estimates a project at $10 million, does it come in on budget? Who wins the contracts? Is there real competition in the bids? And where does most of the money actually go?

To answer those questions, I built a database using publicly available bid tabulations and pay estimate records from Caltrans. The dataset includes 2,292 (*Q1) contracts with bid tabulations from 2019 to 2026, worth a combined $19.25 billion (*Q1). Every line item, every contractor bid, and every payment estimate.

Of those contracts, 1,645 (*Q2) have completed final pay estimates — meaning the actual final cost is known. Another 2,132 (*Q2b) are tracked at the PROGRESS level, and 1,768 (*Q2b) are in AFTER ACCEPTANCE status (warranty/closeout phase). The remaining contracts have no pay estimate records in the system.

Here are the numbers.

## The Big Picture: Scale and Growth

Using the winning bid (rank 1) value, the following table shows all contracts by year. These are awarded amounts — the lowest bids quoted for each project, not final costs.

| Year | Contracts | Completed | In Progress | No PE | Total Value | Avg Contract | Avg Bidders |
|---|---|---|---|---|---|---|---|
| 2019 | 334 | 329 | 5 | 0 | $2.71B | $8,099,968 | 5.3 |
| 2020 | 305 | 294 | 11 | 0 | $2.04B | $6,676,249 | 5.9 |
| 2021 | 344 | 320 | 23 | 1 | $2.30B | $6,677,011 | 5.9 |
| 2022 | 369 | 302 | 66 | 1 | $2.80B | $7,594,216 | 4.8 |
| 2023 | 334 | 241 | 92 | 1 | $2.82B | $8,453,462 | 4.4 |
| 2024 | 295 | 130 | 163 | 2 | $2.83B | $9,599,361 | 5.0 |
| 2025 | 280 | 27 | 142 | 111 | $3.52B | $12,561,362 | 5.7 |
| 2026 | 29 | 0 | 0 | 29 | $243M | $8,144,400 | 5.8 |

(*Q3)

The average contract stands at $8.4 million (*Q1), but that doesn't tell the full story. The smallest contracts are under $65,000 for routine sign work, while the largest contract in the dataset stands at $274.9 million (*Q1).

Awarded contract values increased significantly from 2020 to 2025. Total awarded values climbed from $2.0B in 2020 to $3.5B in 2025, with average contract values growing from $6.7M to over $12.6M. This reflects both inflation in construction costs and an increase in the scale of projects Caltrans is undertaking.

Competition dipped notably in 2022-2023. The average number of bidders fell from 5.9 in 2020-2021 to 4.4 in 2023, before recovering to 5.7 in 2025. Even at the low point, California maintained far higher competition levels than many other state DOTs — for context, Colorado averaged only 2.6-3.6 bidders during the same period.

---

## Where the Money Goes: Spending by District

Caltrans operates through 12 districts, each with its own geography, traffic patterns, and construction challenges.

| District | Name | Contracts | Total Value | Avg Contract | Avg Bidders |
|---|---|---|---|---|---|
| 04 | Oakland / Bay Area | 331 | $3.25B | $9,809,489 | 5.3 |
| 07 | Los Angeles | 300 | $2.60B | $8,672,900 | 6.1 |
| 08 | San Bernardino | 236 | $2.38B | $10,088,810 | 6.2 |
| 03 | Marysville | 247 | $2.25B | $9,112,824 | 5.0 |
| 12 | Irvine / Orange County | 159 | $1.74B | $10,920,033 | 7.0 |
| 06 | Fresno | 212 | $1.60B | $7,550,932 | 4.7 |
| 05 | San Luis Obispo | 163 | $1.08B | $6,648,901 | 4.3 |
| 11 | San Diego | 121 | $1.08B | $8,894,928 | 5.0 |
| 01 | Eureka | 130 | $1.02B | $7,829,795 | 4.8 |
| 10 | Stockton | 174 | $975M | $5,602,581 | 4.9 |
| 02 | Redding | 143 | $804M | $5,621,097 | 4.3 |
| 09 | Bishop | 76 | $480M | $6,310,679 | 3.9 |

(*Q7)

The Bay Area (District 04) leads with $3.25B across 331 contracts. Los Angeles (District 07) is second at $2.60B. Together, the Bay Area and LA represent over 30% of all Caltrans contract dollars.

Southern California's inland empire (District 08 - San Bernardino) has a high average contract value at $10.1M, while also enjoying the second-highest competition level at 6.2 average bidders. Irvine/Orange County (District 12) has the highest average contract value at $10.9M and the most competitive market at 7.0 average bidders.

Rural districts — Bishop (09), Redding (02), and San Luis Obispo (05) — have lower competition (3.9-4.3 bidders) and lower average contract values, consistent with the smaller contractor pool available in those areas.

### Who Dominates Each District?

| District | Name | Top Contractor | Contracts Won | Total Awarded |
|---|---|---|---|---|
| 01 | Eureka | GRANITE CONSTRUCTION COMPANY | 22 | $253M |
| 02 | Redding | HAT CREEK CONSTRUCTION & MATERIALS, INC. | 13 | $126M |
| 03 | Marysville | DESILVA GATES CONSTRUCTION LLC | 4 | $290M |
| 04 | Oakland / Bay Area | BAY CITIES PAVING & GRADING, INC. | 14 | $541M |
| 05 | San Luis Obispo | GRANITE CONSTRUCTION COMPANY | 23 | $275M |
| 06 | Fresno | GRANITE CONSTRUCTION COMPANY | 48 | $397M |
| 07 | Los Angeles | SECURITY PAVING COMPANY, INC. | 6 | $284M |
| 08 | San Bernardino | GRANITE CONSTRUCTION COMPANY | 17 | $363M |
| 09 | Bishop | ROAD AND HIGHWAY BUILDERS, LLC | 2 | $76M |
| 10 | Stockton | BAY CITIES PAVING & GRADING, INC. | 4 | $121M |
| 11 | San Diego | SKANSKA USA CIVIL WEST | 2 | $115M |
| 12 | Irvine / Orange County | SECURITY PAVING COMPANY, INC. | 5 | $368M |

(*Q23)

Granite Construction dominates four districts (01, 05, 06, 08) — more than any other contractor. They are the largest contractor in the dataset by total volume. Bay Cities dominates the Bay Area, Security Paving leads in Southern California (LA and Irvine), and smaller regional players control their home turf (Hat Creek in Redding, DeSilva Gates in Marysville). District 09 (Bishop) is led by Road and Highway Builders — a regional specialist in rural Nevada/California desert work.

---

## Who Wins the Work?

The top 10 contractors account for $6.56 billion (*Q5), which is 34.1% (*Q5) of all awarded dollars, from 400 of 2,292 contracts.

| Contractor | Contracts Won | Total Bids | Win Rate % | Total Awarded |
|---|---|---|---|---|
| GRANITE CONSTRUCTION COMPANY | 147 | 585 | 25.1% | $1,685,593,407 |
| SECURITY PAVING COMPANY, INC. | 25 | 166 | 15.1% | $1,111,884,219 |
| BAY CITIES PAVING & GRADING, INC. | 20 | 49 | 40.8% | $677,271,243 |
| O.C. JONES & SONS, INC. | 50 | 114 | 43.9% | $590,077,325 |
| MYERS & SONS CONSTRUCTION, LLC | 59 | 307 | 19.2% | $554,622,191 |
| GRIFFITH COMPANY | 48 | 208 | 23.1% | $496,406,957 |
| BAY CITIES PAVING & GRADING | 21 | 52 | 40.4% | $468,188,575 |
| GOLDEN STATE BRIDGE, INC. | 22 | 177 | 12.4% | $385,294,373 |
| DESILVA GATES CONSTRUCTION LLC | 5 | 25 | 20.0% | $294,059,772 |
| FLATIRON WEST, INC. | 3 | 30 | 10.0% | $292,926,858 |

(*Q4)

### Granite Construction Company — $1.69 Billion

- **Contracts Won:** 147 (out of 585 total bids — 25.1% win rate) (*Q4)
- **Headquarters:** Watsonville, CA
- **Primary Work:** The dominant contractor statewide. They lead in 4 of 12 districts (Eureka, SLO, Fresno, San Bernardino). They bid on everything — from $100K sign jobs to $100M+ highway projects.
- **Why they win:** Scale, geographic reach, and asphalt plant ownership across the state. They can mobilize to any district.

### Security Paving Company — $1.11 Billion

- **Contracts Won:** 25 (out of 166 total bids — 15.1% win rate) (*Q4)
- **Primary Work:** Large-scale Southern California freeway projects. They lead both LA (District 07) and Orange County (District 12).
- **Why they win:** Despite a low win rate, they win large contracts — their average awarded contract exceeds $44M. They bid aggressively on the mega-projects.

### Bay Cities Paving & Grading — ~$1.15 Billion (combined)

- **Contracts Won:** ~41 combined (40.8% / 40.4% win rate) (*Q4)
- **Primary Work:** Bay Area (District 04) and Central Valley (District 10). High win rate indicates strong competitive positioning.
- **Data note:** Appears as two entries due to inconsistent naming in source PDFs.

### O.C. Jones & Sons — $590 Million

- **Contracts Won:** 50 (out of 114 total bids — 43.9% win rate) (*Q4)
- **Primary Work:** Bay Area construction. High win rate indicates strong competitive positioning.

California's contractor market is more fragmented than Colorado's. The top 10 control 34.1% of spending (*Q5), compared to Colorado where the top 7 controlled 49.3%. California's market supports a deeper bench of qualified firms due to the sheer volume of work.

---

## Do Projects Actually Go Over Budget?

This is the central question. Caltrans's pay estimate system tracks the original contract amount and the total amount earned by the contractor. The difference between total earned and the original contract amount reveals cost growth driven by change orders, extra work, and quantity adjustments.

Across 1,648 (*Q8) completed (FINAL) contracts:

- **Average cost overrun: +13.0%** (*Q8)
- **Median cost overrun: +2.7%** (*Q8)
- **32.8% of projects finished under budget** (*Q8)
- **Net total overrun: $496 million** (*Q8)

The high average (+13.0%) is skewed by a handful of extreme outliers. The median of +2.7% is the more representative measure — meaning the typical Caltrans project grows by about 2.7% from the original contract amount to the final cost.

Using the exact same methodology against Colorado's CDOT (final cost vs. winning bid, FINAL pay estimates, 2014–2024): CDOT finishes 53.9% of projects over budget with a median overrun of +0.7% (*Q35). Caltrans is worse: 67.2% over budget at a median of +2.7%. But context matters. The gap largely comes from extra work. Caltrans contracts with **no extra work** finish 42.9% over budget with a median of **-0.7%** — comparable to CDOT's baseline (*Q36). The real driver is extra work: 82.6% of completed Caltrans contracts carry some extra work (*Q22), and those contracts run 72% over budget at a median of +3.5%. Both systems go over budget more often than not. Caltrans does it more frequently and by more — and extra work spending is the structural reason why.

### Distribution of Overruns

| Overrun Range | Contracts |
|---|---|
| > 50% over budget | 13 |
| 20% to 50% over | 112 |
| 5% to 20% over | 487 |
| 0% to 5% over | 495 |
| Under budget (savings) | 541 |

(*Q9)

Nearly 63% of projects (1,036 of 1,648) are within +5% or under budget. Only 13 projects (0.8%) exceeded 50% overrun.

### The Mega Projects

The most expensive completed Caltrans projects:

| Contract | Contractor | Winning Bid | Final Cost | Overrun $ | Overrun % |
|---|---|---|---|---|---|
| 03-0H10U4 | NOR CAL PAVING | $274,852,000 | $295,612,990 | $20,760,990 | +7.6% |
| 08-1C0824 | FISHER SAND & GRAVEL CO. | $267,839,839 | $266,555,520 | -$1,284,319 | -0.5% |
| 08-1C38U4 | COFFMAN SPECIALTIES, INC | $181,885,000 | $184,631,760 | $2,746,760 | +1.5% |
| 12-0K0224 | FLATIRON WEST, INC. | $129,773,276 | $151,797,433 | $22,024,157 | +17.0% |
| 08-0K1224 | SULLY-MILLER CONTRACTING | $121,672,000 | $143,921,921 | $22,249,921 | +18.3% |

(*Q10)

The two largest completed contracts are both in the $275M range. One (NOR CAL PAVING) came in 7.6% over; the other (FISHER SAND & GRAVEL) came in 0.5% under budget. The largest mega-projects show a mixed pattern — some come in close to budget, while others experience significant growth.

### The Worst Overruns (contracts > $1M)

| Contract | Contractor | Winning Bid | Final Cost | Overrun $ | Overrun % |
|---|---|---|---|---|---|
| 04-3G4544 | — | $14,858,813 | $44,434,385 | $29,575,572 | +199.0% |
| 11-2N0424 | HAZARD CONSTRUCTION | $1,708,547 | $3,263,146 | $1,554,599 | +91.0% |
| 06-0U4704 | — | $24,198,298 | $43,408,610 | $19,210,313 | +79.4% |
| 04-3G6204 | MYERS AND SONS CONSTR. | $20,349,212 | $35,106,551 | $14,757,339 | +72.5% |
| 04-3G4744 | — | $38,401,065 | $65,655,672 | $27,254,607 | +71.0% |

(*Q11)

The worst overrun — contract 04-3G4544 — nearly tripled in cost, growing from $14.9M to $44.4M. Several of the worst overruns are in District 04 (Bay Area), suggesting complex urban construction conditions may contribute to cost growth.

---

## Contractor Efficiency Rankings

### Highest Average Overruns (min 3 FINAL contracts)

| Contractor | Contracts | Avg Overrun % | Total Overrun $ |
|---|---|---|---|
| MARINA LANDSCAPE INC. | 3 | +48.2% | $675,447 |
| SUKUT CONSTRUCTION, LLC | 3 | +23.8% | $4,819,834 |
| DIVERSIFIED LANDSCAPE CO. | 4 | +23.4% | $2,758,402 |
| DIG IT CONSTRUCTION, INC | 3 | +22.2% | $814,821 |
| HAZARD CONSTRUCTION COMPANY | 6 | +17.5% | $2,781,273 |

(*Q12)

### Most Consistent Under Budget (min 3 FINAL contracts)

| Contractor | Contracts | Avg Overrun % | Total Savings $ |
|---|---|---|---|
| HIGHLAND CONSTRUCTION, INC. | 4 | -18.9% | $1,699,231 |
| POLO ENGINEERING, INC. | 4 | -18.6% | $988,827 |
| PAL GENERAL ENGINEERING INC | 5 | -18.4% | $5,328,404 |
| PAPICH CONSTRUCTION CO., INC. | 6 | -16.3% | $4,183,974 |
| SAN PATRICIO CONSTRUCTION | 3 | -15.7% | $857,988 |

(*Q13)

---

## How Accurate Are Caltrans's Engineer Estimates?

Before contractors bid, Caltrans engineers prepare a cost estimate. How close are these estimates to what contractors actually bid?

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

(*Q25)

> **Column notes:** *Median % vs Estimate* — the typical winning bid expressed as a percentage above (+) or below (−) Caltrans's internal pre-bid cost projection. A value of -8.9% means the typical winner bid 8.9% below what engineers estimated. *% Over Estimate* — the share of contracts that year where the winning bid exceeded the engineer estimate. Values below 50% mean most winners bid under estimate; above 50% means most came in over.

- Median winning bid vs. estimate overall: 92.0% — meaning the typical winning bid is 8% below the engineer's estimate (*Q15)
- 67.4% of winning bids came in under the engineer's estimate (*Q15)

In most years, winning bids come in well below the estimate (*Q25). The exception was 2022–2023, when bids crept toward and then crossed the estimate threshold. In 2023, the median winning bid exceeded the engineer estimate for the first time in this dataset (+1.2%), with 51.8% of bids coming in above estimate (*Q25). This aligns directly with peak construction inflation and the lowest competition period in the dataset (4.4 avg bidders, 3.0% sole-bidder rate). By 2025, the pattern fully reversed — bids fell back to 13.5% below estimates (*Q25), confirming that the 2022–2023 period was an anomaly, not a structural shift.

### What the Engineer Estimate Tells You

The engineer's estimate is Caltrans's internal pre-bid cost projection. It functions as a ceiling, not a target — in normal market conditions, competition drives winning bids well below it.

Across the dataset, the median winning bid was **8% below the engineer estimate** (*Q15), and **67.4% of all winning bids** came in under the estimate. Collectively, the gap between estimates and winning bids represents over **$1.27 billion** in competitive savings — money budgeted by Caltrans that the market didn't need to spend.

The 2022-2023 surge tells the same story. When competition fell (4.4 avg bidders, sole-bidder rates tripling) and material costs spiked, bids climbed past estimates. Winning bids and engineer estimates are structurally linked — more competition means lower bids relative to estimate, and the data proves it.

The practical implication: Caltrans's engineer estimates appear realistic. They are not artificially low (which would produce constant bid overruns) or artificially high (which would inflate budgets). When the market is healthy, contractors sharpen pencils and the public gets the discount.

---

## Competition Trends

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

(*Q14)

California's contractor market is remarkably competitive. Even during the 2022-2023 dip, Caltrans averaged 4.4-4.8 bidders per contract with sole-bidder rates of only 1.9-3.0%. Compare this to Colorado, where sole-bidder rates reached 22.2% in 2023.

The highly competitive bid rate (5+ bidders) dropped from 71.5% in 2020 to 38.3% in 2023, then recovered to 66.8% in 2025. This mirrors the national construction market cycle — labor shortages and material cost volatility drove contractors to be more selective in 2022-2023, before competition recovered as conditions stabilized.


### Extra Work and Change Orders

Change orders and extra work add cost and time:

| Contracts w/ Extra Work | Avg Extra Work $ | Total Extra Work $ | Avg Extra Work % | Avg CCO Days |
|---|---|---|---|---|
| 1,359 | $528,972 | $718,872,428 | 18.7% | 10 |

(*Q22)

82.5% of completed contracts (1,359 of 1,648) include extra work — new scope added after the contract was awarded (*Q22). That extra work totals $719 million and averages 18.7% of the original contract amount (*Q22).

Here's the critical finding: on contracts that went over budget, extra work accounts for 101% of all net cost growth (*Q22b). The original contract line items, that weren't in the extra work, actually come in slightly under their authorized amounts on net (-$7.8M) (*Q22b). Every dollar of budget overrun traces back to scope that wasn't in the original contract.

Contracts with extra work have a median overrun of +3.5% and 72% go over budget. Contracts without extra work have a median overrun of -0.7% and only 43% go over budget (*Q22c). This seems to explain what is going on with the overruns.

Once extra work exceeds 10% of the original contract, the project is almost certainly going over budget (94.4%) (*Q22c).
It gets worse as projects get bigger. Every single contract over $25M had extra work added, and the overruns scale accordingly (*Q22d, *Q36):

| Extra Work as % of Contract | Contracts | Avg Cost Overrun | % Over Budget | Avg Additional Days |
|---|---|---|---|---|
| No extra work | 287 | -2.7% | 43.2% | 0.4 |
| Under 5% | 775 | +0.2% | 59.0% | 4.8 |
| 5–10% | 301 | +5.8% | 85.4% | 10.7 |
| 10–20% | 179 | +12.9% | 94.4% | 18.7 |
| 20–50% | 88 | +22.4% | 90.9% | 23.0 |
| 50%+ | 15 | +55.6% | 100.0% | 77.2 |

(*Q22c) *Contracts under $100K excluded to remove data entry outliers.*

| Contract Size | Contracts | Has Extra Work | % Over Budget | Median Overrun |
|---|---|---|---|---|
| Under 1M | 384 | 68.2% | 64.1% | +2.5% |
| 1–5M | 919 | 82.8% | 64.4% | +2.1% |
| 5–10M | 187 | 95.7% | 71.7% | +3.4% |
| 10–25M | 114 | 99.1% | 80.7% | +5.9% |
| Over 25M | 44 | 100.0% | 88.6% | +6.3% |

(*Q22d)

Every single contract over $25M had extra work added. Nearly 9 in 10 went over budget. This isn't necessarily a sign of poor planning — large highway projects are complex enough that unforeseen conditions (utility conflicts, soil issues, design changes requested by local agencies) are almost guaranteed to surface. The question isn't whether extra work will appear, but how much and whether it was foreseeable scope that should have been in the original contract.

---

### What's Driving the Item-Level Overruns?

Comparing original authorized amounts against final paid amounts by item category across all FINAL contracts shows which work types most commonly exceed their budgeted quantities (*Q22e):

| Item Category | Contracts | Gross Overrun $ | Avg Overrun % |
|---|---|---|---|
| Hot Mix Asphalt | 1,147 | $75.3M | +13.2% |
| Roadway Excavation | 665 | $27.8M | +6.3% |
| Time-Related Overhead | 1,369 | $22.5M | +3.3% |
| Cold Plane AC | 795 | $8.5M | +4.3% |
| Aggregate Base | 585 | $6.0M | +5.4% |

(*Q22e)

Paving and earthwork dominate. These are quantity-driven items where actual field conditions often require more material than estimated. The standout is Time-Related Overhead: it carries a net overrun of +$20.4M across all contracts — the financial fingerprint of schedule delays. When projects run long, daily overhead charges accumulate directly on this line item.

Note that Hot Mix Asphalt has a large gross overrun ($75.3M) but a net of **-$46.9M** across all contracts — on many contracts, HMA quantities come in well under bid. It is a high-variance item in both directions.

### Contracts Without Extra Work

Even contracts with zero extra work still see a 42.9% over-budget rate (*Q34). The numbers show these are not a structural problem: the median overrun is **-0.7%** (slightly under budget), the average is **-2.7%**, and 67.5% of these contracts finish within 5% of the original amount in either direction (*Q34). These are routine quantity variances — not systematic cost failures.

---

## Most Worked Highways

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

(*Q17)

I-5 runs the full length of California from Mexico to Oregon — 169 contracts totaling $2.0 billion (*Q17). US-101 along the coast is second at $1.6B, followed by SR-99 through the Central Valley at $947M. I-80 and I-10 round out the top five.

The top two highways — I-5 and US-101 — account for $3.6 billion in construction, roughly 18.7% of all contract value in the dataset (*Q17, *Q1).

---

## So — Is Caltrans Efficient?

After analyzing 2,292 (*Q1) contracts and $19.3 billion (*Q1) in construction spending, here is what the data says.

**The competitive market works.** California's contractor market is remarkably healthy. With an average of 5+ bidders per contract and sole-bidder rates under 3%, Caltrans gets genuine competition on nearly every project. This is far better than many other state DOTs. The median winning bid comes in 8% below the engineer's estimate (*Q15), indicating robust competitive pricing.

**Projects go over budget more often than not.** 67% of completed contracts finish above their winning bid, with a median overrun of +2.7% (*Q8). About half (49.6%) land within ±5% of budget, but 37% run more than 5% over. The average is pulled up by outliers — only 13 projects (0.8%) exceeded 50% overrun. Extra work is the primary driver: averaging 18.7% of original contract amounts (*Q22), it accounts for virtually all of the net cost growth.

**The market is geographically fragmented — and that's healthy.** Unlike states where 3-5 firms dominate statewide, California has distinct regional leaders. Granite controls the Central Coast and Inland Empire. Bay Cities owns the Bay Area. Security Paving dominates Southern California freeways. This geographic fragmentation creates natural competition zones.

**The biggest risk is mega-project overruns.** While the typical project stays near budget, the largest contracts ($100M+) show more variance. The two largest completed projects diverged — one came in 7.6% over, the other 0.5% under. The worst overruns are concentrated in a small number of Bay Area projects.

**Competition dipped in 2022-2023 but recovered.** The 2022-2023 construction inflation period reduced bidding activity. The highly competitive bid rate (5+ bidders) dropped from 71% to 40%. But by 2025, it bounced back to 69%. Caltrans's market proved resilient.

---

## For Contractors

If you build roads for a living in California, this dataset contains years of competitive intelligence:

- Who beats you on which item codes, and in which districts?
- Are you losing because your asphalt price is high or because your mobilization is skewed?
- Do you perform better in certain districts, project sizes, or terrain types?
- Are you bidding too often on jobs you historically have little chance of winning?

This article scratches the surface. The full dataset breaks down bidding performance by item, by district, and by competitor over time.

If you're interested in seeing how your company stacks up, I can generate that analysis.

---

## Author's Note

This analysis is built on the same methodology used for the [CDOT (Colorado) article](link), which analyzed $7.18 billion in Colorado construction contracts. The Caltrans dataset is significantly larger — $19.25 billion vs $7.18 billion — and includes richer data on project lifecycle stages (PROGRESS, AFTER ACCEPTANCE, FINAL) and 2.3 million item-level pay estimate records.

All numbers come directly from Caltrans's publicly available bid tabulations and PETS (Pay Estimate Tracking System) records.

Support this work: buymeacoffee.com/Data.youngblood

**Contact & Support Email:** data.youngblood@gmail.com
