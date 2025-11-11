from backend.utils.validators import clamp

def green_score(total_kg_month: float) -> int:
    # 0..600 kg/month mapped to 0..100 score (lower is better)
    score = 100 - (total_kg_month / 600) * 100
    return int(clamp(score, 0, 100))
