def suggest_loyalty_tier(total_spend: float) -> str:
    if total_spend >= 10000000:
        return "Diamond"
    if total_spend >= 5000000:
        return "Gold"
    if total_spend >= 2000000:
        return "Silver"
    return "Bronze"
