# 🧴 India Men's Premium Body Wash — Market Intelligence

> A data-driven market analysis pipeline that collects live data from Google Trends, Amazon India, and World Bank APIs to size the opportunity and deliver a Go/No-Go investment recommendation for India's men's premium body wash category.

**Verdict: GO ✅ — Score 7.8/10** | Market: ₹1,180 Cr (2025E) | CAGR: 16.2% (2019–2025)

---

## Table of Contents
- [Project Overview](#project-overview)
- [Key Findings](#key-findings)
- [Dashboard Preview](#dashboard-preview)
- [Data Sources](#data-sources)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [How to Run](#how-to-run)
- [Analysis Scripts](#analysis-scripts)

---

## Project Overview

This project builds an end-to-end market intelligence pipeline for India's men's premium body wash segment. It automates data collection from three live sources, processes and cross-references the data, and produces a fully interactive HTML dashboard with a data-backed Go/No-Go recommendation.

**What it answers:**
- How big is the market and how fast is it growing?
- Where are the pricing gaps on Amazon India right now?
- Which brands are gaining or losing search momentum?
- Which Indian states have the highest unmet demand?
- Should a new brand enter this category — and how?

---

## Key Findings

### Market
| Metric | Value |
|--------|-------|
| Market size (2025E) | ₹1,180 Crore |
| CAGR 2019–2025 | 16.2% |
| Premium segment share | 18% (2019) → **41% (2025E)** |
| Online FMCG channel share | 2.1% (2018) → **13.8% (2025)** |

### Amazon India (Live — 404 SKUs analysed)
| Metric | Value |
|--------|-------|
| Median price | ₹303 |
| Average rating | 4.24 ★ |
| **Price gap identified** | ₹300–₹499 tier is **underpenetrated** vs demand |
| Highest discount brand | Bombay Shaving Company |

### Google Trends (Live — 261 weeks, 10 brands)
- **Beardo** is the most-searched D2C grooming brand in India
- D2C brands (Beardo, Ustraa, The Man Company) growing **34–41% YoY** vs 6–14% for mass players
- **"Men's skincare India"** is the fastest-rising category intent signal

### Regional Demand
- Highest composite demand: **Tamil Nadu, Maharashtra, Karnataka, Andhra Pradesh, Delhi NCR**
- Lowest penetration (opportunity): North-East states, smaller tier-2/3 markets

### Go/No-Go Scorecard
```
Market Size & Growth      ██████████████████░░  9/10
Digital Channel Tailwind  ██████████████████░░  9/10
Price Opportunity         ████████████████░░░░  8/10
Demand Signal (Trends)    ████████████████░░░░  8/10
Urban Demographic Runway  ████████████████░░░░  8/10
Regulatory / Entry Ease   ████████████████░░░░  8/10
Amazon Presence Required  ██████████████░░░░░░  7/10
Competitive Intensity     ██████████░░░░░░░░░░  5/10  ← only risk
─────────────────────────────────────────────────────
WEIGHTED AVERAGE          ███████████████░░░░░  7.8/10  →  GO ✅
```

**Recommended entry:** Launch at ₹299–₹399 ("accessible premium") via Amazon + D2C. Lead with South India (TN, KA, KL, AP) and Maharashtra where demand is high and no single brand dominates.

---

## Business Impact Simulation

To estimate whether this category is attractive from an investment perspective, I added a simple revenue simulation based on premium-segment market size and assumed market-share capture.

### Assumptions
- Total market size (2025E): ₹1,180 Cr
- Premium segment share: 41%
- Average selling price (ASP): ₹349
- Revenue estimated under multiple market-share scenarios

### Revenue Scenarios

| Target Share of Premium Segment | Estimated Annual Revenue |
|---|---:|
| 0.5% | ₹2.42 Cr |
| 1.0% | ₹4.84 Cr |
| 2.0% | ₹9.68 Cr |
| 5.0% | ₹24.19 Cr |

### Interpretation
Even a 1–2% share of the premium segment could translate into ~₹4.8–₹9.7 Cr in annual revenue, making the category commercially attractive if customer acquisition and retention economics are favorable.

---

## Dashboard Preview

The final dashboard (`reports/final_analysis.html`) is a self-contained interactive HTML file containing six sections:

| Section | What it shows |
|---------|---------------|
| Market Size & Growth | ₹ Cr timeline, premium share, GDP/capita, CPI, e-commerce penetration |
| Amazon Price Analysis | Violin plots, price vs rating bubble chart, SKU heatmap, discount depth |
| Google Trends | 5-year brand trends, category signals, YoY change, 90-day seasonality |
| Regional Heatmap | India choropleth + top-15 states bar chart from live Trends data |
| Channel & Tier Dynamics | Distribution channel shift 2021→2025; price tier volume/value migration |
| Go/No-Go Scorecard | 8-dimension scored chart, key findings, entry strategy recommendation |

---

## Data Sources

| Source | Method | Records |
|--------|--------|---------|
| **Google Trends** (via pytrends) | Live API | 261 weeks × 10 brands; 36 Indian states; 5 category keywords |
| **Amazon India** | Live web scrape | 435 products — price, rating, review count, ASIN, badge |
| **World Bank API** | Live API | 15 years × 5 macro indicators (GDP, urban %, inflation, consumption) |
| **Open Exchange Rates** | Live API | Real-time USD/INR rate |
| **MOSPI / IAMAI / Annual Reports** | Curated | CPI personal care, e-commerce penetration, FMCG company benchmarks |

All raw data is saved to `data/raw/` as CSV/JSON for reproducibility and offline use.

---

## Project Structure

```
india-grooming-project/
│
├── analysis/                          # All Python scripts
│   ├── collect_google_trends.py       # Pulls live Google Trends data (pytrends)
│   ├── collect_amazon.py              # Scrapes Amazon India product listings
│   ├── collect_public_datasets.py     # World Bank, CPI, channel, tier data
│   ├── market_analysis.py             # Exploratory charts (matplotlib/seaborn)
│   └── build_final_dashboard.py       # Assembles final interactive HTML report
│
├── data/
│   ├── raw/                           # All collected datasets (CSV/JSON)
│   │   ├── amazon_products_raw.csv
│   │   ├── gtrends_brand_interest_over_time.csv
│   │   ├── gtrends_regional_interest.csv
│   │   ├── gtrends_category_trends.csv
│   │   ├── gtrends_seasonal_90d.csv
│   │   ├── worldbank_india_pivot.csv
│   │   ├── india_bodywash_price_tier_distribution.csv
│   │   ├── india_bodywash_channel_distribution.csv
│   │   ├── india_fmcg_company_benchmarks.csv
│   │   ├── india_internet_ecommerce_penetration.csv
│   │   ├── india_cpi_personal_care_static.csv
│   │   └── exchange_rate_usd_inr.csv
│   ├── processed/                     # Cleaned/transformed data
│   └── external/                      # Third-party data
│
├── visualizations/                    # Static chart exports (PNG/HTML)
├── reports/
│   └── final_analysis.html            # ← Main deliverable (self-contained)
├── notebooks/                         # Jupyter notebooks (optional)
│
├── requirements.txt
└── README.md
```

---

## Technologies Used

| Category | Library / Tool | Purpose |
|----------|---------------|---------|
| **Data collection** | `pytrends` 4.9.2 | Google Trends unofficial API |
| | `requests` + `beautifulsoup4` | Amazon India web scraping |
| | `requests` | World Bank & Exchange Rate APIs |
| **Data processing** | `pandas` | DataFrames, cleaning, pivoting |
| | `numpy` | Numerical operations, normalization |
| **Visualization** | `plotly` | Interactive charts & HTML dashboard |
| | `matplotlib` | Static chart exports |
| | `seaborn` | Heatmaps |
| **Output** | Pure HTML/CSS | Self-contained report (no server needed) |
| **Runtime** | Python 3.10+ | — |

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/india-grooming-project.git
cd india-grooming-project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Collect live data
Run the three collectors in order:
```bash
# Google Trends (takes ~2–3 min due to rate limiting)
python analysis/collect_google_trends.py

# Amazon India product listings
python analysis/collect_amazon.py

# World Bank, CPI, FMCG benchmarks
python analysis/collect_public_datasets.py
```

> **Note:** Google Trends and Amazon may occasionally return 429/503 errors due to rate limiting. Re-run after a few minutes if this happens. Pre-collected data is included in `data/raw/` so you can skip to step 4.

### 4. Build the dashboard
```bash
python analysis/build_final_dashboard.py
```

### 5. Open the report
```bash
open reports/final_analysis.html        # macOS
start reports/final_analysis.html       # Windows
xdg-open reports/final_analysis.html    # Linux
```

Or simply double-click `reports/final_analysis.html` in your file explorer. No server required — it is fully self-contained.

---

## Analysis Scripts

| Script | What it does | Runtime |
|--------|-------------|---------|
| `collect_google_trends.py` | Fetches 5-year weekly interest for 10 brands, 36 Indian states, and 5 category keywords | ~3 min |
| `collect_amazon.py` | Scrapes product title, price, MRP, rating, review count, ASIN for 8 brand queries × 2 pages | ~4 min |
| `collect_public_datasets.py` | Calls World Bank API, saves CPI/channel/tier/FMCG reference data | ~30 sec |
| `market_analysis.py` | Generates exploratory matplotlib/seaborn charts to `visualizations/` | ~10 sec |
| `build_final_dashboard.py` | Loads all raw data, builds 6-section Plotly dashboard, writes HTML | ~15 sec |

---

## License

MIT — free to use, adapt, and extend for your own market research projects.

---

*Data refreshed: March 2026 · Exchange rate: ₹92.55/USD · Built with Python + Plotly*
