import pandas as pd
import plotly.express as px
from pathlib import Path

# ----------------------------
# Assumptions
# ----------------------------
TOTAL_MARKET_CR = 1180
PREMIUM_SHARE = 0.41
ASP = 349

share_scenarios = [0.005, 0.01, 0.02, 0.05]

premium_market_cr = TOTAL_MARKET_CR * PREMIUM_SHARE

rows = []

for share in share_scenarios:
    revenue_cr = premium_market_cr * share
    revenue_inr = revenue_cr * 10_000_000
    units = revenue_inr / ASP

    rows.append({
        "market_share_pct": share * 100,
        "estimated_revenue_cr": round(revenue_cr, 2),
        "estimated_revenue_inr": round(revenue_inr, 0),
        "estimated_units": round(units, 0)
    })

df = pd.DataFrame(rows)

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

df.to_csv(output_dir / "business_impact_simulation.csv", index=False)

fig = px.line(
    df,
    x="market_share_pct",
    y="estimated_revenue_cr",
    markers=True,
    title="Revenue Potential by Premium Segment Market Share",
    labels={
        "market_share_pct": "Target Share (%)",
        "estimated_revenue_cr": "Revenue (₹ Cr)"
    }
)

fig.write_html("visualizations/business_impact_simulation.html")

print(df)
