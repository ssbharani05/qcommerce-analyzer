# 🛒 Q-Commerce Entry Analyzer

> **Should your D2C brand enter Blinkit, Zepto, or Swiggy Instamart?**
> A data-driven profitability tool built for Indian D2C brands navigating the 2026 quick commerce landscape.

Live Tool: https://qcommerce-analyzer-lbm2shxfnffcrjezpnfwj2.streamlit.app/

---

## The Problem

68% of Indian D2C brands fail to break even on quick commerce platforms.
Platform fees, commissions, and minimum ad spends silently eat margins — most brands find out too late.

This tool gives brands a Go/No-Go verdict before they spend a single rupee.

---

## How It Works

Enter your brand's unit economics:
- Cost of Goods Sold (COGS)
- Average Order Value (AOV)
- Customer Acquisition Cost (CAC)
- Expected monthly orders
- Number of SKUs and product category

The tool instantly outputs:
- GO / CAUTION / NO-GO verdict per platform
- Profitability score out of 100
- Full cost breakdown (commission, fulfillment, ad spend, listing fees)
- Visual comparison across all 3 platforms

---

## Platforms Analyzed

| Platform | Market Share | Commission | Min Ad Spend |
|---|---|---|---|
| Blinkit | 50% | 18% | 2,50,000 per month |
| Zepto | 29% | 20% | 5,00,000 per month |
| Swiggy Instamart | 23% | 15% | 2,00,000 per month |

Data based on public platform disclosures and industry reports 2026.

---

## Project Structure

- data/platform_data.json — Mock API with real 2026 platform data
- calculator.py — Core profitability logic
- app.py — Streamlit web app
- analysis.ipynb — BA analysis notebook with charts
- requirements.txt — Dependencies

---

## Run Locally

git clone https://github.com/ssbharani05/qcommerce-analyzer.git
cd qcommerce-analyzer
pip install -r requirements.txt
streamlit run app.py

---

## Key Insights

- Brands with AOV below 600 need 2000+ monthly orders to survive on any platform
- Instamart is the best entry point for new brands — lowest minimum ad spend
- Zepto suits only well-funded brands — 5L per month minimum ad spend
- FMCG and Personal Care are the highest fit categories scoring 8-9 out of 10
- Fashion and Electronics should avoid Q-Commerce entirely scoring 2-3 out of 10

---

## About

Built by Bharanidhar S — Business Analyst | Marketing Analytics
