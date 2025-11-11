def load_efs():
    return {
        "elec": 0.82,  # kg CO₂ per kWh
        "natural_gas": 5.3,  # kg CO₂ per therm
        "car": 0.21,   # kg CO₂ per km
        "bus": 0.09,   # kg CO₂ per km
        "food": {
            "veg": 120,     # kg CO₂ per month
            "mixed": 160,   # kg CO₂ per month  
            "nonveg": 216   # kg CO₂ per month
        }
    }