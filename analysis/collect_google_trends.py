"""
Google Trends data collector for India men's grooming market.
Uses pytrends (unofficial Google Trends API).
"""

import time
import pandas as pd
import os

# Patch urllib3 Retry for pytrends compatibility with urllib3 v2.x
import urllib3.util.retry as _retry_mod
_OrigRetry = _retry_mod.Retry
class _PatchedRetry(_OrigRetry):
    def __init__(self, *args, method_whitelist=None, **kwargs):
        if method_whitelist is not None:
            kwargs.setdefault("allowed_methods", method_whitelist)
        super().__init__(*args, **kwargs)
_retry_mod.Retry = _PatchedRetry

from pytrends.request import TrendReq

OUT = os.path.join(os.path.dirname(__file__), "../data/raw")
os.makedirs(OUT, exist_ok=True)

pytrends = TrendReq(hl="en-IN", tz=330, timeout=(10, 25), retries=2, backoff_factor=0.5)

# ---------------------------------------------------------------------------
# 1. Interest over time — brand keywords
# ---------------------------------------------------------------------------

BRAND_KEYWORDS = [
    ["Dove Men Care", "Nivea Men", "Beardo", "Ustraa", "The Man Company"],
    ["Old Spice body wash", "Fiama Men", "Park Avenue body wash",
     "Bombay Shaving Company", "Wild Stone body wash"],
]

all_interest = []
print("Fetching brand interest over time...")
for group in BRAND_KEYWORDS:
    pytrends.build_payload(group, cat=0, timeframe="today 5-y", geo="IN")
    df = pytrends.interest_over_time()
    if not df.empty:
        df = df.drop(columns=["isPartial"], errors="ignore")
        all_interest.append(df)
    time.sleep(3)

if all_interest:
    combined = pd.concat(all_interest, axis=1)
    combined = combined.loc[:, ~combined.columns.duplicated()]
    combined.index.name = "date"
    combined.reset_index(inplace=True)
    path = os.path.join(OUT, "gtrends_brand_interest_over_time.csv")
    combined.to_csv(path, index=False)
    print(f"  Saved {combined.shape} → {path}")

# ---------------------------------------------------------------------------
# 2. Interest by region (India states)
# ---------------------------------------------------------------------------

print("Fetching regional interest...")
pytrends.build_payload(["men body wash", "men grooming"], timeframe="today 12-m", geo="IN")
region_df = pytrends.interest_by_region(resolution="REGION", inc_low_vol=True, inc_geo_code=False)
if not region_df.empty:
    region_df = region_df.reset_index()
    path = os.path.join(OUT, "gtrends_regional_interest.csv")
    region_df.to_csv(path, index=False)
    print(f"  Saved {region_df.shape} → {path}")

time.sleep(3)

# ---------------------------------------------------------------------------
# 3. Related queries — discover consumer intent
# ---------------------------------------------------------------------------

print("Fetching related queries...")
pytrends.build_payload(["men body wash india", "mens grooming india"],
                       timeframe="today 12-m", geo="IN")
related = pytrends.related_queries()
rows = []
for kw, data in related.items():
    for qtype in ("top", "rising"):
        if data and data.get(qtype) is not None:
            df = data[qtype].copy()
            df["keyword"] = kw
            df["type"] = qtype
            rows.append(df)
if rows:
    rq = pd.concat(rows, ignore_index=True)
    path = os.path.join(OUT, "gtrends_related_queries.csv")
    rq.to_csv(path, index=False)
    print(f"  Saved {rq.shape} → {path}")

time.sleep(3)

# ---------------------------------------------------------------------------
# 4. Trending searches — grooming category
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS = [
    "men body wash",
    "premium body wash",
    "men shower gel india",
    "men grooming products",
    "men skincare india",
]

print("Fetching category trend over time...")
pytrends.build_payload(CATEGORY_KEYWORDS, timeframe="today 5-y", geo="IN")
cat_df = pytrends.interest_over_time()
if not cat_df.empty:
    cat_df = cat_df.drop(columns=["isPartial"], errors="ignore").reset_index()
    path = os.path.join(OUT, "gtrends_category_trends.csv")
    cat_df.to_csv(path, index=False)
    print(f"  Saved {cat_df.shape} → {path}")

time.sleep(3)

# ---------------------------------------------------------------------------
# 5. Seasonal / monthly breakdown (90-day window)
# ---------------------------------------------------------------------------

print("Fetching seasonal data...")
pytrends.build_payload(["men body wash", "men grooming"], timeframe="today 3-m", geo="IN")
season_df = pytrends.interest_over_time()
if not season_df.empty:
    season_df = season_df.drop(columns=["isPartial"], errors="ignore").reset_index()
    path = os.path.join(OUT, "gtrends_seasonal_90d.csv")
    season_df.to_csv(path, index=False)
    print(f"  Saved {season_df.shape} → {path}")

print("\nGoogle Trends collection complete.")
