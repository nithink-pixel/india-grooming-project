"""
Amazon India product data collector.
Scrapes publicly visible search result pages for men's body wash.
Respects crawl delays and only reads data visible to any browser user.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import os
import json

OUT = os.path.join(os.path.dirname(__file__), "../data/raw")
os.makedirs(OUT, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)

SEARCH_QUERIES = [
    "men+premium+body+wash",
    "men+shower+gel+india",
    "beardo+body+wash",
    "dove+men+care+body+wash",
    "nivea+men+body+wash",
    "ustraa+body+wash",
    "the+man+company+body+wash",
    "bombay+shaving+company+body+wash",
    "fiama+men+body+wash",
    "old+spice+body+wash",
]

BASE_URL = "https://www.amazon.in/s?k={query}&i=beauty"


def parse_price(text):
    if not text:
        return None
    nums = re.findall(r"[\d,]+", text.replace(",", ""))
    return int(nums[0]) if nums else None


def parse_rating(text):
    if not text:
        return None
    m = re.search(r"([\d.]+)", text)
    return float(m.group(1)) if m else None


def scrape_search_page(query, page=1):
    url = BASE_URL.format(query=query)
    if page > 1:
        url += f"&page={page}"
    try:
        resp = SESSION.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"  Request failed for '{query}' p{page}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "lxml")

    # Check for CAPTCHA / bot detection
    if "Enter the characters you see below" in resp.text or "captcha" in resp.text.lower():
        print(f"  CAPTCHA detected for '{query}' — skipping")
        return []

    products = []
    cards = soup.select('[data-component-type="s-search-result"]')

    for card in cards:
        try:
            # Title
            title_el = card.select_one("h2 span")
            title = title_el.get_text(strip=True) if title_el else None

            # Brand (from title or byline)
            brand_el = card.select_one(".a-row.a-size-base.a-color-secondary span")
            brand = brand_el.get_text(strip=True) if brand_el else None

            # Price
            price_el = card.select_one(".a-price .a-offscreen")
            price = parse_price(price_el.get_text() if price_el else None)

            # MRP / original price
            mrp_el = card.select_one(".a-price.a-text-price .a-offscreen")
            mrp = parse_price(mrp_el.get_text() if mrp_el else None)

            # Rating
            rating_el = card.select_one(".a-icon-alt")
            rating = parse_rating(rating_el.get_text() if rating_el else None)

            # Review count
            reviews_el = card.select_one('[aria-label*="ratings"]') or card.select_one(".a-size-base.s-underline-text")
            review_count = None
            if reviews_el:
                m = re.search(r"([\d,]+)", reviews_el.get_text())
                if m:
                    review_count = int(m.group(1).replace(",", ""))

            # Sponsored flag
            sponsored = bool(card.select_one(".s-label-popover-default"))

            # ASIN
            asin = card.get("data-asin", None)

            # Badge (Amazon's Choice, Best Seller)
            badge_el = card.select_one(".a-badge-text")
            badge = badge_el.get_text(strip=True) if badge_el else None

            if title:
                products.append({
                    "asin": asin,
                    "title": title,
                    "brand": brand,
                    "price_inr": price,
                    "mrp_inr": mrp,
                    "rating": rating,
                    "review_count": review_count,
                    "sponsored": sponsored,
                    "badge": badge,
                    "search_query": query.replace("+", " "),
                })
        except Exception:
            continue

    return products


all_products = []
for query in SEARCH_QUERIES:
    print(f"Scraping: {query.replace('+', ' ')}")
    for page in [1, 2]:
        results = scrape_search_page(query, page)
        print(f"  Page {page}: {len(results)} products")
        all_products.extend(results)
        time.sleep(2.5)
    time.sleep(3)

if all_products:
    df = pd.DataFrame(all_products)
    # Deduplicate by ASIN (keep first occurrence with most data)
    df_dedup = df.dropna(subset=["asin"])
    df_dedup = df_dedup.sort_values("review_count", ascending=False).drop_duplicates("asin")
    # Also keep rows without ASIN (rare)
    df_no_asin = df[df["asin"].isna() | (df["asin"] == "")]
    final = pd.concat([df_dedup, df_no_asin], ignore_index=True)

    path = os.path.join(OUT, "amazon_products_raw.csv")
    final.to_csv(path, index=False)
    print(f"\nSaved {final.shape[0]} unique products → {path}")

    # Summary stats
    summary = {
        "total_products": int(final.shape[0]),
        "with_price": int(final["price_inr"].notna().sum()),
        "with_rating": int(final["rating"].notna().sum()),
        "avg_price_inr": round(float(final["price_inr"].dropna().mean()), 2),
        "avg_rating": round(float(final["rating"].dropna().mean()), 2),
        "price_range": {
            "min": int(final["price_inr"].dropna().min()),
            "max": int(final["price_inr"].dropna().max()),
            "median": int(final["price_inr"].dropna().median()),
        },
    }
    jpath = os.path.join(OUT, "amazon_collection_summary.json")
    with open(jpath, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary → {jpath}")
    print(json.dumps(summary, indent=2))
else:
    print("\nNo products collected — Amazon may have blocked requests.")
    print("Consider using Amazon Product Advertising API with credentials.")

print("\nAmazon collection complete.")
