import json
import os

def load_platform_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "platform_data.json")
    with open(data_path, "r") as f:
        return json.load(f)

def calculate_profitability(cogs, aov, cac, monthly_orders, num_skus, category, platform_key):
    data = load_platform_data()
    platform = data["platforms"][platform_key]
    category_data = data["category_benchmarks"].get(category, None)
    gross_revenue = aov * monthly_orders
    commission = gross_revenue * platform["commission_rate"]
    fulfillment = platform["fulfillment_fee_per_order"] * monthly_orders
    ad_spend = platform["min_monthly_ad_spend"]
    listing_cost = (platform["listing_fee_per_sku"] * num_skus) / 12
    total_platform_cost = commission + fulfillment + ad_spend + listing_cost
    total_cogs = cogs * monthly_orders
    total_cac = cac * monthly_orders
    total_cost = total_cogs + total_cac + total_platform_cost
    net_profit = gross_revenue - total_cost
    profit_margin = (net_profit / gross_revenue) * 100 if gross_revenue > 0 else 0
    platform_take_rate = (total_platform_cost / gross_revenue) * 100
    score = 0
    if profit_margin > 20:
        score += 40
    elif profit_margin > 10:
        score += 30
    elif profit_margin > 0:
        score += 15
    if category_data:
        fit = category_data["qcommerce_fit_score"]
        score += int((fit / 10) * 30)
    if platform_take_rate < 35:
        score += 30
    elif platform_take_rate < 50:
        score += 20
    elif platform_take_rate < 70:
        score += 10
    if score >= 70:
        verdict = "✅ GO"
        verdict_detail = "Strong profitability. This platform suits your brand."
    elif score >= 45:
        verdict = "⚠️ PROCEED WITH CAUTION"
        verdict_detail = "Marginal profitability. Optimize costs before scaling."
    else:
        verdict = "❌ NO-GO"
        verdict_detail = "Platform costs will likely exceed your margins."
    return {
        "platform": platform["name"],
        "category": category,
        "gross_revenue": gross_revenue,
        "total_platform_cost": total_platform_cost,
        "platform_take_rate": round(platform_take_rate, 2),
        "net_profit": round(net_profit, 2),
        "profit_margin": round(profit_margin, 2),
        "score": score,
        "verdict": verdict,
        "verdict_detail": verdict_detail,
        "breakdown": {
            "commission": round(commission, 2),
            "fulfillment": round(fulfillment, 2),
            "ad_spend": ad_spend,
            "listing_cost_monthly": round(listing_cost, 2),
            "cogs_total": round(total_cogs, 2),
            "cac_total": round(total_cac, 2)
        }
    }

def analyze_all_platforms(cogs, aov, cac, monthly_orders, num_skus, category):
    results = {}
    for platform_key in ["blinkit", "zepto", "instamart"]:
        results[platform_key] = calculate_profitability(
            cogs, aov, cac, monthly_orders, num_skus, category, platform_key
        )
    return results
