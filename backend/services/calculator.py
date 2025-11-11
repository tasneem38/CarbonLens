from backend.utils.ef_loader import load_efs

EFS = load_efs()

def compute_footprint(payload: dict) -> dict:
    # Extract values with defaults
    electricity_kwh = payload.get("electricityKwh", 0)
    natural_gas_therms = payload.get("naturalGasTherms", 0)
    car_km = payload.get("carKm", 0)
    bus_km = payload.get("busKm", 0)
    diet = payload.get("diet", "mixed")
    food_emissions = payload.get("foodEmissions", 0)
    goods_emissions = payload.get("goodsEmissions", 0)
    
    # Calculate energy emissions (electricity + natural gas)
    elec = electricity_kwh * EFS["elec"]
    gas = natural_gas_therms * EFS.get("natural_gas", 5.3)  # Fallback if not in EFS
    energy = elec + gas
    
    # Calculate travel emissions
    car = car_km * EFS["car"]
    bus = bus_km * EFS["bus"]
    travel = car + bus
    
    # Calculate food emissions - use foodEmissions if provided, otherwise use diet
    if food_emissions > 0:
        # Convert daily food emission factor to monthly (assuming 30 days)
        food = food_emissions * 30
    else:
        # Use traditional diet-based calculation
        food = EFS["food"][diet]
    
    # Include goods emissions
    goods = goods_emissions
    
    # Calculate total
    total = round(energy + travel + food + goods, 1)
    
    return {
        "total": total,
        "energy": round(energy, 1),
        "travel": round(travel, 1),
        "food": round(food, 1),
        "goods": round(goods, 1),
    }