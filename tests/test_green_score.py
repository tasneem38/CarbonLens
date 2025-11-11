from backend.services.scoring import green_score

def test_green_score_bounds():
    assert 0 <= green_score(0) <= 100
    assert 0 <= green_score(600) <= 100
