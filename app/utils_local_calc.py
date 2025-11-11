import math

EF = {
    "electricity": 0.82,  # kg CO₂ per kWh
    "natural_gas": 5.3,   # kg CO₂ per therm
    "car_km": 0.21,       # kg CO₂ per km
    "bus_km": 0.09,       # kg CO₂ per km
    "food_per_day": {"Vegan": 1.5, "Vegetarian": 2.0, "Pescatarian": 2.5, 
                    "Flexitarian": 3.0, "Omnivore (balanced)": 3.5, "Omnivore (meat-heavy)": 4.5}  # kg CO₂ per day
}

def _score_from_total(total_kg: float) -> int:
    # Enhanced scoring: 100 is great, 0 is poor; 800 kg/mo considered baseline upper bound
    # More realistic scoring for comprehensive inputs
    s = round(max(0, min(100, 100 - (total_kg/800)*100)))
    return int(s)

def local_compute(inputs: dict) -> dict:
    # Calculate energy emissions (electricity + natural gas)
    elec = inputs.get("electricityKwh", 0) * EF["electricity"]
    gas = inputs.get("naturalGasTherms", 0) * EF["natural_gas"]
    energy = elec + gas
    
    # Calculate travel emissions (car + bus)
    travel = inputs.get("carKm", 0) * EF["car_km"] + inputs.get("busKm", 0) * EF["bus_km"]
    
    # Calculate food emissions based on foodEmissions factor (kg CO₂ per day)
    food_emissions_factor = inputs.get("foodEmissions", 3.5)  # Default to balanced omnivore
    food = food_emissions_factor * 30  # Convert daily rate to monthly
    
    # Include goods emissions directly
    goods = inputs.get("goodsEmissions", 0)
    
    # Calculate total emissions
    total = round(energy + travel + food + goods, 1)
    score = _score_from_total(total)

    # Generate trend data
    trend = [{"x": f"M{i+1}", "y": round(max(150, total + math.sin(i/2)*60), 1)} for i in range(12)]
    
    # Determine diet type for recommendations
    diet_types = list(EF["food_per_day"].keys())
    current_diet = None
    current_factor = inputs.get("foodEmissions", 3.5)
    
    for diet, factor in EF["food_per_day"].items():
        if abs(current_factor - factor) < 0.1:
            current_diet = diet
            break
    
    if not current_diet:
        current_diet = "your current diet"
    
    return {
        "inputs": inputs,
        "totals": {
            "total": total, 
            "energy": round(energy, 1), 
            "travel": round(travel, 1), 
            "food": round(food, 1),
            "goods": round(goods, 1)
        },
        "score": score,
        "trend": trend,
        "recommendations": [
            {
                "area": "Energy",
                "text": f"Reduce electricity usage by 15% to save {round(elec * 0.15, 1)} kg CO₂/month",
                "impact_kg_month": round(elec * 0.15, 1),
                "confidence": 0.85
            },
            {
                "area": "Travel", 
                "text": f"Switch 30% of car trips to public transport to save {round(inputs.get('carKm', 0) * 0.3 * (EF['car_km'] - EF['bus_km']), 1)} kg CO₂/month",
                "impact_kg_month": round(inputs.get('carKm', 0) * 0.3 * (EF['car_km'] - EF['bus_km']), 1),
                "confidence": 0.80
            },
            {
                "area": "Food",
                "text": f"Consider shifting from {current_diet} to a more plant-based diet",
                "impact_kg_month": round(food * 0.2, 1),
                "confidence": 0.75
            },
            {
                "area": "Shopping",
                "text": "Reduce consumption of new goods and choose sustainable products",
                "impact_kg_month": round(goods * 0.1, 1),
                "confidence": 0.70
            }
        ]
    }

def simulate_with_sliders(base_inputs: dict, car_reduce_pct: int, elec_reduce_pct: int, diet_shift_pct: int):
    # Calculate baseline emissions
    elec_base = base_inputs.get("electricityKwh", 0) * EF["electricity"]
    gas_base = base_inputs.get("naturalGasTherms", 0) * EF["natural_gas"]
    car_base = base_inputs.get("carKm", 0) * EF["car_km"]
    bus_base = base_inputs.get("busKm", 0) * EF["bus_km"]
    food_base = base_inputs.get("foodEmissions", 3.5) * 30  # Monthly conversion
    goods_base = base_inputs.get("goodsEmissions", 0)
    
    before = {
        "Energy": elec_base + gas_base,
        "Travel": car_base + bus_base,
        "Food": food_base,
        "Goods": goods_base,
    }
    
    # Calculate emissions after reductions
    elec_after = elec_base * (1 - elec_reduce_pct/100)
    car_after = car_base * (1 - car_reduce_pct/100)
    food_after = food_base * (1 - diet_shift_pct/100)
    
    after = {
        "Energy": elec_after + gas_base,  # Gas remains same
        "Travel": car_after + bus_base,   # Bus remains same
        "Food": food_after,
        "Goods": goods_base,              # Goods remain same
    }
    
    return before, after