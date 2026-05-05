import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from calculator import analyze_all_platforms
import json

# --- Page Config ---
st.set_page_config(
    page_title="Q-Commerce Entry Analyzer",
    page_icon="🛒",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    .main { background-color: #0f0f0f; }
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .verdict-go { background: #0d3b0d; border-left: 4px solid #00ff00; padding: 15px; border-radius: 8px; }
    .verdict-caution { background: #3b2e00; border-left: 4px solid #ffcc00; padding: 15px; border-radius: 8px; }
    .verdict-nogo { background: #3b0d0d; border-left: 4px solid #ff3333; padding: 15px; border-radius: 8px; }
    .metric-card { background: #1a1a1a; padding: 20px; border-radius: 10px; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.title("🛒 Q-Commerce Entry Analyzer")
st.markdown("**Should your D2C brand enter Blinkit, Zepto, or Instamart?**")
st.markdown("*Built for Indian D2C brands navigating the 2026 quick commerce landscape*")
st.divider()

# --- Sidebar Inputs ---
st.sidebar.header("📊 Your Brand Inputs")
st.sidebar.markdown("Enter your brand's numbers to get a Go/No-Go verdict.")

cogs = st.sidebar.number_input(
    "Cost of Goods Sold per unit (₹)",
    min_value=10, max_value=10000, value=150, step=10,
    help="What does it cost you to make/source one unit?"
)

aov = st.sidebar.number_input(
    "Average Order Value (₹)",
    min_value=100, max_value=10000, value=500, step=50,
    help="Average amount a customer spends per order"
)

cac = st.sidebar.number_input(
    "Customer Acquisition Cost per order (₹)",
    min_value=0, max_value=5000, value=80, step=10,
    help="What you spend to acquire one customer/order"
)

monthly_orders = st.sidebar.number_input(
    "Expected Monthly Orders",
    min_value=100, max_value=100000, value=500, step=100,
    help="How many orders do you expect per month on the platform?"
)

num_skus = st.sidebar.number_input(
    "Number of SKUs",
    min_value=1, max_value=500, value=5, step=1,
    help="How many unique products you plan to list"
)

category = st.sidebar.selectbox(
    "Product Category",
    ["FMCG", "Personal Care", "Snacks", "Beverages", "Beauty", "Grocery", "Fashion", "Electronics"],
    help="Choose the category that best fits your product"
)

analyze_btn = st.sidebar.button("🚀 Analyze Now", use_container_width=True)

# --- Main Area ---
if analyze_btn:
    with st.spinner("Running profitability analysis across all platforms..."):
        results = analyze_all_platforms(cogs, aov, cac, monthly_orders, num_skus, category)

    st.subheader("📋 Platform Verdicts")
    cols = st.columns(3)
    platform_keys = ["blinkit", "zepto", "instamart"]
    colors = {"✅ GO": "verdict-go", "⚠️ PROCEED WITH CAUTION": "verdict-caution", "❌ NO-GO": "verdict-nogo"}

    for i, key in enumerate(platform_keys):
        r = results[key]
        css_class = colors.get(r["verdict"], "verdict-caution")
        with cols[i]:
            st.markdown(f"""
                <div class="{css_class}">
                    <h3>{r['platform']}</h3>
                    <h2>{r['verdict']}</h2>
                    <p>{r['verdict_detail']}</p>
                    <hr style="border-color:#444">
                    <b>Score:</b> {r['score']}/100<br>
                    <b>Net Profit/month:</b> ₹{r['net_profit']:,.0f}<br>
                    <b>Profit Margin:</b> {r['profit_margin']}%<br>
                    <b>Platform Take Rate:</b> {r['platform_take_rate']}%
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- Score Comparison Chart ---
    st.subheader("📊 Platform Score Comparison")
    df_scores = pd.DataFrame({
        "Platform": [results[k]["platform"] for k in platform_keys],
        "Score": [results[k]["score"] for k in platform_keys],
        "Verdict": [results[k]["verdict"] for k in platform_keys]
    })

    fig_bar = px.bar(
        df_scores, x="Platform", y="Score", color="Score",
        color_continuous_scale=["#ff3333", "#ffcc00", "#00ff00"],
        range_color=[0, 100], text="Score"
    )
    fig_bar.update_layout(
        paper_bgcolor="#0f0f0f", plot_bgcolor="#1a1a1a",
        font_color="white", showlegend=False
    )
    fig_bar.add_hline(y=70, line_dash="dash", line_color="#00ff00", annotation_text="GO threshold (70)")
    fig_bar.add_hline(y=45, line_dash="dash", line_color="#ffcc00", annotation_text="Caution threshold (45)")
    st.plotly_chart(fig_bar, use_container_width=True)

    # --- Cost Breakdown ---
    st.subheader("💸 Cost Breakdown by Platform")
    breakdown_data = []
    for key in platform_keys:
        b = results[key]["breakdown"]
        breakdown_data.append({
            "Platform": results[key]["platform"],
            "COGS": b["cogs_total"],
            "Commission": b["commission"],
            "Fulfillment": b["fulfillment"],
            "Ad Spend": b["ad_spend"],
            "CAC": b["cac_total"],
            "Listing Cost": b["listing_cost_monthly"]
        })

    df_breakdown = pd.DataFrame(breakdown_data).set_index("Platform")
    fig_stack = px.bar(
        df_breakdown.reset_index().melt(id_vars="Platform"),
        x="Platform", y="value", color="variable",
        barmode="stack", labels={"value": "₹ Cost", "variable": "Cost Type"}
    )
    fig_stack.update_layout(
        paper_bgcolor="#0f0f0f", plot_bgcolor="#1a1a1a", font_color="white"
    )
    st.plotly_chart(fig_stack, use_container_width=True)

    # --- Detailed Table ---
    st.subheader("📄 Detailed Numbers")
    df_table = pd.DataFrame([{
        "Platform": results[k]["platform"],
        "Gross Revenue (₹)": f"₹{results[k]['gross_revenue']:,.0f}",
        "Total Platform Cost (₹)": f"₹{results[k]['total_platform_cost']:,.0f}",
        "Net Profit (₹)": f"₹{results[k]['net_profit']:,.0f}",
        "Profit Margin": f"{results[k]['profit_margin']}%",
        "Platform Take Rate": f"{results[k]['platform_take_rate']}%",
        "Score": f"{results[k]['score']}/100",
        "Verdict": results[k]["verdict"]
    } for k in platform_keys])
    st.dataframe(df_table, use_container_width=True, hide_index=True)

else:
    st.info("👈 Enter your brand's numbers in the sidebar and click **Analyze Now** to get your Go/No-Go verdict.")
    st.markdown("""
    ### How this works
    This tool analyzes whether your D2C brand can profitably operate on Blinkit, Zepto, or Swiggy Instamart — based on their real 2026 commission structures, fees, and your brand's unit economics.

    **Inputs you need:**
    - Your product's Cost of Goods Sold (COGS)
    - Your Average Order Value (AOV)
    - Your Customer Acquisition Cost (CAC)
    - Expected monthly orders
    - Number of SKUs & product category

    **Output:**
    - Go / Caution / No-Go verdict per platform
    - Profitability score out of 100
    - Full cost breakdown & visual comparison
    """)

st.divider()
st.caption("Built by Bharanidhar S | Q-Commerce BA Project 2026 | Data based on public sources & platform disclosures")