import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from calculator import analyze_all_platforms

st.set_page_config(
    page_title="Q-Commerce Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Mono', monospace;
    background-color: #080b10;
    color: #e8f0fe;
}

.stApp { background-color: #080b10; }

section[data-testid="stSidebar"] {
    background-color: #0d1117;
    border-right: 1px solid rgba(0,240,180,0.1);
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    line-height: 1;
    color: #e8f0fe;
    margin-bottom: 0.25rem;
}

.hero-accent {
    color: transparent;
    -webkit-text-stroke: 1.5px #00f0b4;
}

.hero-sub {
    color: #6b7fa0;
    font-size: 0.8rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

.stat-row {
    display: flex;
    gap: 2rem;
    margin: 1.5rem 0;
    padding: 1.2rem 1.5rem;
    background: #0d1117;
    border: 1px solid rgba(0,240,180,0.1);
    border-left: 3px solid #00f0b4;
}

.stat-item { text-align: center; }
.stat-num {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.6rem;
    color: #00f0b4;
}
.stat-label {
    font-size: 0.65rem;
    color: #6b7fa0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.verdict-go {
    background: linear-gradient(135deg, #0a2a1a, #0d3b22);
    border: 1px solid #00ff88;
    border-top: 3px solid #00ff88;
    padding: 1.5rem;
    border-radius: 2px;
    margin-bottom: 1rem;
}
.verdict-caution {
    background: linear-gradient(135deg, #2a2010, #3b2e00);
    border: 1px solid #ffcc00;
    border-top: 3px solid #ffcc00;
    padding: 1.5rem;
    border-radius: 2px;
    margin-bottom: 1rem;
}
.verdict-nogo {
    background: linear-gradient(135deg, #2a0a0a, #3b0d0d);
    border: 1px solid #ff4444;
    border-top: 3px solid #ff4444;
    padding: 1.5rem;
    border-radius: 2px;
    margin-bottom: 1rem;
}

.platform-name {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7fa0;
    margin-bottom: 0.5rem;
}

.verdict-badge {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.4rem;
    margin-bottom: 1rem;
}

.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin: 1rem 0;
}

.metric-item {
    background: rgba(0,0,0,0.3);
    padding: 0.6rem 0.8rem;
    border-radius: 2px;
}

.metric-label {
    font-size: 0.6rem;
    color: #6b7fa0;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: #e8f0fe;
}

.why-box {
    background: rgba(0,0,0,0.2);
    border-left: 2px solid rgba(255,255,255,0.1);
    padding: 0.75rem 1rem;
    margin-top: 1rem;
    font-size: 0.75rem;
    color: #8a9bc0;
    line-height: 1.6;
}

.section-tag {
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #00f0b4;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-tag::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 1px;
    background: #00f0b4;
}

.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.4rem;
    margin-bottom: 1.5rem;
    color: #e8f0fe;
}

.score-bar-bg {
    background: #1a1a2e;
    border-radius: 1px;
    height: 6px;
    margin-top: 0.5rem;
    overflow: hidden;
}

.insight-box {
    background: #0d1117;
    border: 1px solid rgba(0,240,180,0.1);
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    border-radius: 2px;
}

.insight-number {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    color: #00f0b4;
    opacity: 0.3;
    float: left;
    margin-right: 1rem;
    line-height: 1;
}

.stButton > button {
    background: transparent;
    border: 1px solid #00f0b4;
    color: #00f0b4;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.75rem 2rem;
    width: 100%;
    transition: all 0.2s;
}

.stButton > button:hover {
    background: #00f0b4;
    color: #080b10;
}

div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    font-size: 0.7rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #6b7fa0 !important;
}

.footer-text {
    font-size: 0.65rem;
    color: #3a4a60;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    text-align: center;
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(0,240,180,0.05);
}
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-tag">Input Parameters</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Brand Economics</div>', unsafe_allow_html=True)

    cogs = st.number_input("COGS per unit (₹)", min_value=10, max_value=10000, value=150, step=10)
    aov = st.number_input("Avg Order Value (₹)", min_value=100, max_value=10000, value=500, step=50)
    cac = st.number_input("Customer Acq. Cost (₹)", min_value=0, max_value=5000, value=80, step=10)
    monthly_orders = st.number_input("Monthly Orders", min_value=100, max_value=100000, value=2000, step=100)
    num_skus = st.number_input("Number of SKUs", min_value=1, max_value=500, value=5, step=1)
    category = st.selectbox("Product Category", [
        "FMCG", "Personal Care", "Snacks", "Beverages",
        "Beauty", "Grocery", "Fashion", "Electronics"
    ])

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("⚡ Run Analysis")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.65rem; color:#3a4a60; line-height:1.8;'>
    Data based on 2026 platform<br>
    disclosures & industry reports.<br>
    For strategic guidance only.
    </div>
    """, unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">Q-Commerce <span class="hero-accent">Analyzer</span></div>
<div class="hero-sub">⚡ D2C Platform Entry Intelligence — India 2026</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-row">
    <div class="stat-item">
        <div class="stat-num">$7.6B</div>
        <div class="stat-label">Market GMV FY25</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">40%</div>
        <div class="stat-label">YoY Growth</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">68%</div>
        <div class="stat-label">D2C Brands Fail to Break Even</div>
    </div>
    <div class="stat-item">
        <div class="stat-num">42%</div>
        <div class="stat-label">Avg Platform Take Rate</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

def get_why(platform_key, r):
    take = r["platform_take_rate"]
    margin = r["profit_margin"]
    breakdown = r["breakdown"]

    if platform_key == "zepto":
        return f"Zepto's ₹5,00,000 minimum monthly ad spend alone consumes {round(breakdown['ad_spend']/r['gross_revenue']*100,1)}% of your revenue before a single unit ships. At {take}% platform take rate, this platform is commercially indefensible unless your monthly orders exceed 8,000+."
    elif platform_key == "blinkit":
        if margin < 0:
            return f"Blinkit's {round(r['breakdown']['commission']/r['gross_revenue']*100,1)}% commission + ₹{breakdown['fulfillment']:,.0f} fulfillment + ₹{breakdown['ad_spend']:,} ad spend adds up to {take}% take rate. You need a higher AOV product mix (₹600+) or 3,500+ monthly orders to break even here."
        else:
            return f"Blinkit's premium urban audience aligns with your category. At {take}% take rate, margins are tight but viable. Focus on high-AOV SKUs and optimize ad spend to improve score above 70."
    elif platform_key == "instamart":
        if margin > 0:
            return f"Instamart's lowest fee structure ({take}% take rate) makes it the only viable entry point. Swiggy's existing food delivery base gives organic discovery advantage. Start here, prove unit economics, then expand."
        else:
            return f"Despite being the most affordable platform, Instamart's costs still exceed your current margins. Increasing monthly orders to 3,000+ or raising AOV by ₹100 would flip this to profitable."

# ── RESULTS ──────────────────────────────────────────────
if analyze_btn:
    with st.spinner("Running platform analysis..."):
        results = analyze_all_platforms(cogs, aov, cac, monthly_orders, num_skus, category)

    platform_keys = ["blinkit", "zepto", "instamart"]
    css_map = {
        "✅ GO": "verdict-go",
        "⚠️ PROCEED WITH CAUTION": "verdict-caution",
        "❌ NO-GO": "verdict-nogo"
    }

    st.markdown('<div class="section-tag">Platform Verdicts</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Go / No-Go Analysis</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, key in enumerate(platform_keys):
        r = results[key]
        css = css_map.get(r["verdict"], "verdict-caution")
        why = get_why(key, r)
        profit_color = "#00ff88" if r["net_profit"] > 0 else "#ff4444"
        score_pct = r["score"]

        with cols[i]:
            st.markdown(f"""
            <div class="{css}">
                <div class="platform-name">{r['platform']}</div>
                <div class="verdict-badge">{r['verdict']}</div>
                <div class="score-bar-bg">
                    <div style="width:{score_pct}%; height:100%; background:{'#00ff88' if score_pct>=70 else '#ffcc00' if score_pct>=45 else '#ff4444'}; transition:width 1s;"></div>
                </div>
                <div style="font-size:0.65rem; color:#6b7fa0; margin:0.3rem 0 1rem;">Score: {score_pct}/100</div>
                <div class="metric-grid">
                    <div class="metric-item">
                        <div class="metric-label">Net Profit/mo</div>
                        <div class="metric-value" style="color:{profit_color}">₹{r['net_profit']:,.0f}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Margin</div>
                        <div class="metric-value" style="color:{profit_color}">{r['profit_margin']}%</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Platform Take</div>
                        <div class="metric-value">{r['platform_take_rate']}%</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Revenue/mo</div>
                        <div class="metric-value">₹{r['gross_revenue']:,.0f}</div>
                    </div>
                </div>
                <div class="why-box">
                    <span style="color:#00f0b4; font-size:0.6rem; text-transform:uppercase; letter-spacing:0.1em;">WHY THIS VERDICT</span><br><br>
                    {why}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # Score chart
    st.markdown('<div class="section-tag">Comparison</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Platform Score Breakdown</div>', unsafe_allow_html=True)

    df_scores = pd.DataFrame({
        "Platform": [results[k]["platform"] for k in platform_keys],
        "Score": [results[k]["score"] for k in platform_keys],
        "Net Profit": [results[k]["net_profit"] for k in platform_keys],
        "Take Rate": [results[k]["platform_take_rate"] for k in platform_keys]
    })

    fig = go.Figure()
    bar_colors = []
    for k in platform_keys:
        s = results[k]["score"]
        bar_colors.append("#00ff88" if s >= 70 else "#ffcc00" if s >= 45 else "#ff4444")

    fig.add_trace(go.Bar(
        x=df_scores["Platform"],
        y=df_scores["Score"],
        marker_color=bar_colors,
        text=[f"{s}/100" for s in df_scores["Score"]],
        textposition="outside",
        textfont=dict(color="white", family="Space Mono"),
        name="Score"
    ))

    fig.add_hline(y=70, line_dash="dash", line_color="#00ff88",
                  annotation_text="GO threshold", annotation_font_color="#00ff88")
    fig.add_hline(y=45, line_dash="dash", line_color="#ffcc00",
                  annotation_text="CAUTION threshold", annotation_font_color="#ffcc00")

    fig.update_layout(
        paper_bgcolor="#080b10",
        plot_bgcolor="#0d1117",
        font=dict(color="#e8f0fe", family="Space Mono"),
        showlegend=False,
        height=380,
        margin=dict(t=20, b=20),
        yaxis=dict(range=[0, 110], gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Cost breakdown
    st.markdown('<div class="section-tag">Cost Structure</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Where Your Money Goes</div>', unsafe_allow_html=True)

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
            "Listing": b["listing_cost_monthly"]
        })

    df_b = pd.DataFrame(breakdown_data).set_index("Platform")
    fig2 = px.bar(
        df_b.reset_index().melt(id_vars="Platform"),
        x="Platform", y="value", color="variable",
        barmode="stack",
        labels={"value": "₹ Cost", "variable": ""},
        color_discrete_sequence=["#00f0b4","#00aaff","#ff6b6b","#ffcc00","#aa44ff","#ff9944"]
    )
    fig2.update_layout(
        paper_bgcolor="#080b10",
        plot_bgcolor="#0d1117",
        font=dict(color="#e8f0fe", family="Space Mono"),
        height=380,
        margin=dict(t=20, b=20),
        legend=dict(orientation="h", y=-0.2),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Key insights
    st.divider()
    st.markdown('<div class="section-tag">Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key Insights</div>', unsafe_allow_html=True)

    best = max(platform_keys, key=lambda k: results[k]["score"])
    worst = min(platform_keys, key=lambda k: results[k]["score"])
    best_r = results[best]
    worst_r = results[worst]

    insights = [
        f"Best platform for your brand is <b>{best_r['platform']}</b> with a score of {best_r['score']}/100 — {best_r['verdict']}",
        f"Avoid <b>{worst_r['platform']}</b> — {worst_r['platform_take_rate']}% platform take rate makes it commercially unviable at current volumes",
        f"Your effective margin on best platform is <b>{best_r['profit_margin']}%</b> vs your gross margin before platform costs",
        f"To hit GO on all platforms, target <b>AOV above ₹{aov+150}</b> or orders above <b>{monthly_orders+2000:,}/month</b>"
    ]

    for idx, insight in enumerate(insights, 1):
        st.markdown(f"""
        <div class="insight-box">
            <span class="insight-number">0{idx}</span>
            <div style="font-size:0.8rem; line-height:1.7; padding-top:0.2rem;">{insight}</div>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown('<div class="section-tag">How It Works</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Enter Your Numbers. Get Your Answer.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#6b7fa0; font-size:0.8rem; line-height:2; max-width:600px;">
    This tool models the real cost of selling on India's three major
    quick commerce platforms — Blinkit, Zepto and Swiggy Instamart —
    against your brand's unit economics.<br><br>
    It calculates commission, fulfillment fees, minimum ad spend and
    listing costs, then outputs a Go/No-Go score out of 100 with a
    full cost breakdown and plain-English explanation of the verdict.
    </div>
    <br>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    steps = [
        ("01", "Enter Brand Inputs", "COGS, AOV, CAC, monthly orders, SKUs and category in the sidebar"),
        ("02", "Run Analysis", "Click ⚡ Run Analysis to model profitability across all 3 platforms"),
        ("03", "Get Your Verdict", "Go / Caution / No-Go with score, cost breakdown and explanation")
    ]
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="insight-box">
                <span class="insight-number">{num}</span>
                <div style="padding-top:0.2rem;">
                    <div style="font-family:'Syne',sans-serif; font-weight:700; font-size:0.9rem; margin-bottom:0.5rem;">{title}</div>
                    <div style="font-size:0.75rem; color:#6b7fa0; line-height:1.7;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-text">
    Built by Bharanidhar S · Q-Commerce BA Project 2026 · 
    Data from public platform disclosures & industry reports
</div>
""", unsafe_allow_html=True)