import yaml
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Data Assumptions & Sources", page_icon="🔍", layout="wide")
st.markdown('<div class="page-title">Data Assumptions & Sources</div>', unsafe_allow_html=True)

EF_PATH = Path(__file__).resolve().parents[2] / "config" / "emission_factors.yaml"
try:
    with open(EF_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
except Exception:
    data = {
        "electricity": {"india_avg_kg_per_kwh": 0.82, "source": "CEA Baseline v18"},
        "transport": {"car_kg_per_km": 0.21, "bus_kg_per_km": 0.09, "source": "IEA/MoEFCC"},
        "food": {"veg_month_kg": 120, "mixed_month_kg": 160, "nonveg_month_kg": 216, "source": "FAO/IPCC"},
    }

st.write("Below are the emission factors and references currently used by CarbonLens:")
st.markdown(f"""
<div class="card">
  <h4>⚡ Electricity</h4>
  <p><b>{data["factors"]["electricity_kg_per_kwh"]} kg CO₂</b> per kWh</p>
</div>
<div class="card">
  <h4>🚗 Travel</h4>
  <p>Car: {data["factors"]["travel"]["car_kg_per_km"]} kg/km<br>
     Bus: {data["factors"]["travel"]["bus_kg_per_km"]} kg/km<br>
     Train: {data["factors"]["travel"]["train_kg_per_km"]} kg/km
  </p>
</div>
<div class="card">
  <h4>🍽️ Monthly Food Emissions</h4>
  <p>Vegetarian: {data["factors"]["food_monthly_kg"]["veg"]} kg<br>
     Mixed: {data["factors"]["food_monthly_kg"]["mixed"]} kg<br>
     Non-Veg: {data["factors"]["food_monthly_kg"]["nonveg"]} kg
  </p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
**Disclaimer:** These are **estimates** derived from reputable sources (IPCC, IEA, CEA India, FAO).  
Actual emissions vary by location, grid mix, and behavior.
""")
