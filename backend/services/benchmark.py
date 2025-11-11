NATIONAL_AVG_TON_YR = 2.0  # India approx; adjust in config if needed

def compare_to_benchmark(total_kg_month: float) -> dict:
    user_ton_yr = total_kg_month * 12 / 1000
    delta_pct = (user_ton_yr - NATIONAL_AVG_TON_YR) / NATIONAL_AVG_TON_YR * 100
    return {"user_ton_year": round(user_ton_yr, 2), "delta_pct_vs_national": round(delta_pct, 1)}
