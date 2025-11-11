from backend.services.calculator import compute_footprint

def test_compute_footprint_basic():
    totals = compute_footprint({"electricity_kwh":200,"car_km":250,"bus_km":100,"diet":"mixed"})
    assert "total" in totals
    assert totals["total"] > 0
