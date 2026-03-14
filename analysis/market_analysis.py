"""
India Men's Premium Body Wash Market Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Output directory for visualizations
VIZ_DIR = os.path.join(os.path.dirname(__file__), "../visualizations")
os.makedirs(VIZ_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Sample dataset — replace with real data in data/raw/
# ---------------------------------------------------------------------------

brands = pd.DataFrame({
    "brand": [
        "Dove Men+Care", "Nivea Men", "Fiama Men", "Park Avenue",
        "Beardo", "Ustraa", "Old Spice", "Bombay Shaving Company",
        "The Man Company", "Wild Stone"
    ],
    "segment": [
        "Mass Premium", "Mass Premium", "Mass Premium", "Mass Premium",
        "Premium D2C", "Premium D2C", "Mass Premium", "Premium D2C",
        "Premium D2C", "Mass Premium"
    ],
    "avg_price_inr": [220, 195, 175, 160, 349, 329, 150, 399, 379, 130],
    "market_share_pct": [22, 18, 12, 10, 8, 7, 9, 5, 5, 4],
    "online_sales_pct": [45, 38, 30, 25, 82, 88, 28, 91, 89, 22],
    "yoy_growth_pct": [14, 11, 8, 5, 34, 29, 6, 41, 37, 3],
    "parent_company": [
        "Unilever", "Beiersdorf", "ITC", "J.K. Helene Curtis",
        "Beardo (Marico)", "Ustraa", "P&G", "BSC", "TMC", "CavinKare"
    ],
})

market_size = pd.DataFrame({
    "year": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "market_size_cr": [480, 510, 560, 680, 820, 985, 1180],
    "premium_share_pct": [18, 19, 22, 26, 31, 36, 41],
})


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def market_growth_chart():
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax2 = ax1.twinx()

    ax1.bar(market_size["year"], market_size["market_size_cr"],
            color="#2196F3", alpha=0.7, label="Market Size (₹ Cr)")
    ax2.plot(market_size["year"], market_size["premium_share_pct"],
             color="#FF5722", marker="o", linewidth=2, label="Premium Share %")

    ax1.set_xlabel("Year")
    ax1.set_ylabel("Market Size (₹ Crore)")
    ax2.set_ylabel("Premium Segment Share (%)")
    ax1.set_title("India Men's Body Wash Market Growth (2019–2025)")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "market_growth.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def market_share_chart():
    fig = px.pie(
        brands,
        names="brand",
        values="market_share_pct",
        title="Market Share — India Men's Premium Body Wash (2025)",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    path = os.path.join(VIZ_DIR, "market_share.html")
    fig.write_html(path)
    print(f"Saved: {path}")


def price_vs_growth_chart():
    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        brands["avg_price_inr"],
        brands["yoy_growth_pct"],
        s=brands["market_share_pct"] * 50,
        c=brands["online_sales_pct"],
        cmap="RdYlGn",
        alpha=0.8,
        edgecolors="grey",
        linewidth=0.5,
    )
    for _, row in brands.iterrows():
        ax.annotate(row["brand"], (row["avg_price_inr"], row["yoy_growth_pct"]),
                    textcoords="offset points", xytext=(6, 4), fontsize=8)
    plt.colorbar(scatter, ax=ax, label="Online Sales %")
    ax.set_xlabel("Average Price (₹)")
    ax.set_ylabel("YoY Growth (%)")
    ax.set_title("Price vs Growth (bubble size = market share, color = online mix)")
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "price_vs_growth.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def segment_comparison_chart():
    seg = brands.groupby("segment").agg(
        avg_price=("avg_price_inr", "mean"),
        avg_growth=("yoy_growth_pct", "mean"),
        total_share=("market_share_pct", "sum"),
        avg_online=("online_sales_pct", "mean"),
    ).reset_index()

    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Avg Price by Segment", "Avg YoY Growth by Segment"))
    for i, col in enumerate(["avg_price", "avg_growth"], start=1):
        fig.add_trace(
            go.Bar(x=seg["segment"], y=seg[col],
                   marker_color=["#2196F3", "#FF5722"],
                   showlegend=False),
            row=1, col=i,
        )
    fig.update_layout(title_text="Mass Premium vs D2C Premium Segment Comparison")
    path = os.path.join(VIZ_DIR, "segment_comparison.html")
    fig.write_html(path)
    print(f"Saved: {path}")


def brand_heatmap():
    metrics = brands.set_index("brand")[
        ["avg_price_inr", "market_share_pct", "online_sales_pct", "yoy_growth_pct"]
    ]
    normalized = (metrics - metrics.min()) / (metrics.max() - metrics.min())

    plt.figure(figsize=(9, 7))
    sns.heatmap(normalized, annot=metrics.values, fmt=".0f",
                cmap="YlOrRd", linewidths=0.5, cbar_kws={"label": "Normalized Score"})
    plt.title("Brand Metrics Heatmap (raw values annotated)")
    plt.tight_layout()
    path = os.path.join(VIZ_DIR, "brand_heatmap.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"Saved: {path}")


def print_summary():
    print("\n=== MARKET SUMMARY ===")
    print(f"Total brands tracked : {len(brands)}")
    print(f"Market size 2025 est : ₹{market_size.iloc[-1]['market_size_cr']:,} Cr")
    print(f"Premium share 2025   : {market_size.iloc[-1]['premium_share_pct']}%")
    print(f"\nTop 3 by market share:")
    print(brands.nlargest(3, "market_share_pct")[["brand", "market_share_pct", "avg_price_inr"]].to_string(index=False))
    print(f"\nTop 3 by YoY growth:")
    print(brands.nlargest(3, "yoy_growth_pct")[["brand", "yoy_growth_pct", "segment"]].to_string(index=False))
    d2c = brands[brands["segment"] == "Premium D2C"]
    print(f"\nD2C segment avg online sales: {d2c['online_sales_pct'].mean():.0f}%")
    print(f"D2C segment avg YoY growth  : {d2c['yoy_growth_pct'].mean():.0f}%")


if __name__ == "__main__":
    print("Running India Men's Premium Body Wash Market Analysis...")
    market_growth_chart()
    market_share_chart()
    price_vs_growth_chart()
    segment_comparison_chart()
    brand_heatmap()
    print_summary()
    print("\nDone. Check the visualizations/ folder for output files.")
