from backend.services.recommender import recommend_actions

def test_recommendations_energy_heavy():
    recos = recommend_actions({"totals":{"energy":200,"travel":50,"food":120}, "profile":"energy-heavy"})
    assert len(recos) > 0
