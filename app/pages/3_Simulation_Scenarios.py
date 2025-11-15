# app/pages/3_Simulation_Scenarios.py
import streamlit as st
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="What-If Scenarios", page_icon="🕹️", layout="wide")

# --- CSS (small, safe tweaks only) ---
st.markdown(
    """
    <style>
    .card { background: rgba(30,41,59,0.85); border-radius:12px; padding:16px; color: #e6eef2; }
    .small-muted { color:#94a3b8; font-size:13px; }
    .metric-big { font-size:28px; font-weight:800; color:#f1f5f9; }
    .subtle { color:#94a3b8; }
    .two-col { display:flex; gap:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Helper: fallback sample footprint if analyzer hasn't run ---
def get_actual_footprint_or_demo():
    """
    Expected footprint structure:
    {
        "inputs": { ... }, 
        "totals": {"total":..., "energy":..., "travel":..., "food":..., "goods":...},
        "score": int
    }
    """
    if "last_result" in st.session_state:
        try:
            return st.session_state.last_result
        except Exception:
            pass
    # Demo fallback (student housing-like)
    demo = {
        "inputs": {
            "electricityKwh": 180,
            "naturalGasTherms": 10,
            "carKm": 40,
            "busKm": 120,
            "foodEmissions": 2.0,  # per day representative factor
            "goodsEmissions": 80,
            "residents": 3,
            "heating_type": "Electric"
        },
        "totals": {
            "total": 520,
            "energy": 210,
            "travel": 110,
            "food": 150,
            "goods": 50
        },
        "score": 68
    }
    return demo

# --- Simulation engine (simple, deterministic estimator) ---
def simulate(base_inputs, car_pct, elec_pct, diet_pct, renewables_pct, waste_pct, air_pct, shop_pct):
    """
    base_inputs: dict of actual inputs (kWh, carKm, busKm, foodEmissions, goodsEmissions)
    percentages are ints 0-100 representing fraction reduction/adoption
    returns: (before_dict, after_dict, estimated_score)
    """
    # Convert base inputs to rough kg CO2 contributions (use simple multipliers)
    # These multipliers are coarse, but match earlier approximations in app
    electricity_factor = 0.82  # kgCO2/kWh
    gas_factor_per_therm = 5.3  # kgCO2/therm (if used)
    car_factor = 0.21  # per km
    bus_factor = 0.09
    # FoodEmissions: assume this is kgCO2 per day * 30 => monthly
    # goodsEmissions: monthly kgCO2 directly provided

    elec_kwh = base_inputs.get("electricityKwh", 0)
    gas_therms = base_inputs.get("naturalGasTherms", 0)
    car_km = base_inputs.get("carKm", 0)
    bus_km = base_inputs.get("busKm", 0)
    food_daily_factor = base_inputs.get("foodEmissions", 3.5)
    goods = base_inputs.get("goodsEmissions", 0)

    # BEFORE (monthly)
    energy_before = elec_kwh * electricity_factor + gas_therms * gas_factor_per_therm
    travel_before = car_km * car_factor + bus_km * bus_factor
    food_before = food_daily_factor * 30  # monthly
    goods_before = goods
    total_before = energy_before + travel_before + food_before + goods_before

    # Apply adjustments -> AFTER
    # Reductions: car_pct, elec_pct (reduces usage), diet_pct reduces food emissions, renewables_pct reduces electricity portion
    energy_after = energy_before * (1 - elec_pct / 100.0) * (1 - renewables_pct / 200.0)  # renewable shift halves remaining grid-intensity effect
    travel_after = travel_before * (1 - car_pct / 100.0)  # assumes car_pct reduces car travel equivalent
    food_after = food_before * (1 - diet_pct / 100.0) * (1 - waste_pct / 200.0)
    goods_after = goods_before * (1 - shop_pct / 100.0)
    total_after = max(0.0, energy_after + travel_after + food_after + goods_after)

    # Estimate green score: inverse mapping: higher total -> lower score, clamp 0-100
    # Use baseline = total_before; improvement = (before - after)/before
    improvement = (total_before - total_after) / total_before if total_before > 0 else 0
    # Map baseline score roughly from before's magnitude (this is heuristic)
    baseline_score = st.session_state.get("last_result", {}).get("score", None)
    if baseline_score is None:
        # derive a rough baseline score (100 - normalized total)
        # choose normalization pivot = 600 (approx); adjust
        baseline_score = max(10, min(95, 100 - (total_before / 600.0) * 100))
    estimated_score = min(100, max(0, baseline_score + improvement * 40))  # improvement weight

    before = {
        "Energy": round(energy_before, 1),
        "Travel": round(travel_before, 1),
        "Food": round(food_before, 1),
        "Goods": round(goods_before, 1)
    }
    after = {
        "Energy": round(energy_after, 1),
        "Travel": round(travel_after, 1),
        "Food": round(food_after, 1),
        "Goods": round(goods_after, 1)
    }

    return before, after, round(estimated_score, 1)

# --- get actual / demo footprint ---
actual = get_actual_footprint_or_demo()
inputs = actual.get("inputs", {})
totals = actual.get("totals", {})
current_score = actual.get("score", 0)

st.markdown("<h2 style='color:#f1f5f9;'>🕹️ What-If Simulator</h2>", unsafe_allow_html=True)
st.markdown("<div class='small-muted'>Simulate lifestyle changes and watch your 'After' footprint and estimated Green Score update in real-time.</div>", unsafe_allow_html=True)
st.markdown("---")

# ----- TOP: 3-column layout for Before Pie, After Pie, and Green Score -----
col_before, col_after, col_score = st.columns([1, 1, 0.7])

# initialize slider state defaults
if "sim_car" not in st.session_state:
    st.session_state.sim_car = 0
if "sim_elec" not in st.session_state:
    st.session_state.sim_elec = 0
if "sim_diet" not in st.session_state:
    st.session_state.sim_diet = 0
if "sim_renew" not in st.session_state:
    st.session_state.sim_renew = 0
if "sim_waste" not in st.session_state:
    st.session_state.sim_waste = 0
if "sim_air" not in st.session_state:
    st.session_state.sim_air = 0
if "sim_shop" not in st.session_state:
    st.session_state.sim_shop = 0

# compute initial simulation using session_state sliders
before_vals, after_vals, est_score = simulate(
    inputs,
    st.session_state.sim_car,
    st.session_state.sim_elec,
    st.session_state.sim_diet,
    st.session_state.sim_renew,
    st.session_state.sim_waste,
    st.session_state.sim_air,
    st.session_state.sim_shop,
)

# BEFORE pie
with col_before:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-weight:800; font-size:16px;'>Actual (Before)</div>", unsafe_allow_html=True)
    labels = list(before_vals.keys())
    values = list(before_vals.values())
    fig_b = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4, textinfo='label+percent')])
    fig_b.update_layout(margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor='rgba(0,0,0,0)', font_color='#e6eef2')
    st.plotly_chart(fig_b, use_container_width=True)
    st.markdown(f"<div class='small-muted'>Total (monthly): <b>{sum(values):.1f} kg CO₂</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# AFTER pie (updates when sliders change)
with col_after:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div style='font-weight:800; font-size:16px;'>Simulated (After)</div>", unsafe_allow_html=True)
    labels_a = list(after_vals.keys())
    values_a = list(after_vals.values())
    fig_a = go.Figure(data=[go.Pie(labels=labels_a, values=values_a, hole=0.4, textinfo='label+percent')])
    fig_a.update_layout(margin=dict(t=10,b=10,l=10,r=10), paper_bgcolor='rgba(0,0,0,0)', font_color='#e6eef2')
    st.plotly_chart(fig_a, use_container_width=True)
    st.markdown(f"<div class='small-muted'>Total (monthly): <b>{sum(values_a):.1f} kg CO₂</b></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# SCORE card
with col_score:
    st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Current Green Score</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-big'>{current_score}/100</div>", unsafe_allow_html=True)
    st.markdown("<hr />", unsafe_allow_html=True)
    st.markdown("<div class='subtle'>Estimated After Score</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:28px; font-weight:800; color:#00d4aa;'>{est_score}/100</div>", unsafe_allow_html=True)
    improvement_pct = (est_score - current_score)
    if improvement_pct > 0:
        st.success(f"Projected +{improvement_pct:.1f} points")
    elif improvement_pct < 0:
        st.error(f"Projected {improvement_pct:.1f} points")
    else:
        st.info("No change projected")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ----- Settings area: two-column (left sliders, right estimated metrics) -----
left, right = st.columns([2, 1])

with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<b>Customize adjustments</b>", unsafe_allow_html=True)
    # Presets
    preset = st.radio("Preset", ["Custom", "Eco Beginner", "Green Warrior", "Minimalist"], index=0, horizontal=True)
    if preset != "Custom":
        if preset == "Eco Beginner":
            defaults = {"car": 25, "elec": 20, "diet": 20, "renew": 20, "waste": 20, "air": 0, "shop": 10}
        elif preset == "Green Warrior":
            defaults = {"car": 50, "elec": 50, "diet": 50, "renew": 50, "waste": 50, "air": 25, "shop": 30}
        else:  # Minimalist
            defaults = {"car": 75, "elec": 75, "diet": 75, "renew": 75, "waste": 75, "air": 50, "shop": 50}
        # apply defaults to session_state
        st.session_state.sim_car = defaults["car"]
        st.session_state.sim_elec = defaults["elec"]
        st.session_state.sim_diet = defaults["diet"]
        st.session_state.sim_renew = defaults["renew"]
        st.session_state.sim_waste = defaults["waste"]
        st.session_state.sim_air = defaults["air"]
        st.session_state.sim_shop = defaults["shop"]
        st.experimental_rerun()  # rerun so sliders reflect preset
    # Sliders (live)
    st.markdown("#### Transport & Travel")
    st.session_state.sim_car = st.slider("Reduce car usage (%)", 0, 100, int(st.session_state.sim_car), key="sim_car")
    st.session_state.sim_air = st.slider("Reduce air travel (%)", 0, 100, int(st.session_state.sim_air), key="sim_air")

    st.markdown("#### Home & Energy")
    st.session_state.sim_elec = st.slider("Reduce electricity usage (%)", 0, 100, int(st.session_state.sim_elec), key="sim_elec")
    st.session_state.sim_renew = st.slider("Renewables adoption (%)", 0, 100, int(st.session_state.sim_renew), key="sim_renew")

    st.markdown("#### Food & Consumption")
    st.session_state.sim_diet = st.slider("Shift to plant-based diet (%)", 0, 100, int(st.session_state.sim_diet), key="sim_diet")
    st.session_state.sim_waste = st.slider("Reduce food waste (%)", 0, 100, int(st.session_state.sim_waste), key="sim_waste")
    st.session_state.sim_shop = st.slider("Reduce shopping/consumption (%)", 0, 100, int(st.session_state.sim_shop), key="sim_shop")

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<b>Estimated Outcome</b>", unsafe_allow_html=True)
    # recompute using updated sliders
    before_vals, after_vals, est_score = simulate(
        inputs,
        st.session_state.sim_car,
        st.session_state.sim_elec,
        st.session_state.sim_diet,
        st.session_state.sim_renew,
        st.session_state.sim_waste,
        st.session_state.sim_air,
        st.session_state.sim_shop,
    )
    st.markdown("<div style='margin-top:8px;'><span class='small-muted'>Total Before</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700; font-size:20px;'>{sum(before_vals.values()):.1f} kg CO₂ / mo</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:8px;'><span class='small-muted'>Total After</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700; font-size:20px; color:#00d4aa;'>{sum(after_vals.values()):.1f} kg CO₂ / mo</div>", unsafe_allow_html=True)
    st.markdown("<hr />", unsafe_allow_html=True)
    st.markdown(f"<div class='small-muted'>Estimated Green Score</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:28px; font-weight:800; color:#00d4aa;'>{est_score}/100</div>", unsafe_allow_html=True)
    delta = est_score - current_score
    if delta > 0:
        st.success(f"Projected improvement: +{delta:.1f} pts")
    elif delta < 0:
        st.error(f"Projected change: {delta:.1f} pts")
    else:
        st.info("No projected change")
    # quick tips
    st.markdown("<hr />", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'><b>Quick tips</b></div>", unsafe_allow_html=True)
    tips = []
    if st.session_state.sim_car >= 50: tips.append("High car reduction — consider cycling & transit.")
    if st.session_state.sim_elec >= 50: tips.append("Big electricity savings — check insulation & efficient appliances.")
    if st.session_state.sim_diet >= 50: tips.append("Plant-forward diet — try 3 meat-free days/week.")
    for t in tips[:4]:
        st.markdown(f"- <span class='subtle'>{t}</span>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# ----- COMPARISON VISUALS (bar charts before vs after) -----
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<b>Comparison: Before vs After (per category)</b>", unsafe_allow_html=True)
cats = list(before_vals.keys())
before_list = [before_vals[c] for c in cats]
after_list = [after_vals[c] for c in cats]

fig_cmp = go.Figure()
fig_cmp.add_trace(go.Bar(name="Before", x=cats, y=before_list))
fig_cmp.add_trace(go.Bar(name="After", x=cats, y=after_list))
fig_cmp.update_layout(barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#e6eef2')
st.plotly_chart(fig_cmp, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ----- Save scenario / apply scenario (store in session) -----
col_save, col_apply = st.columns([1,1])
with col_save:
    if st.button("Save Scenario"):
        st.session_state["saved_simulation"] = {
            "before": before_vals,
            "after": after_vals,
            "est_score": est_score,
            "sliders": {
                "car": st.session_state.sim_car,
                "elec": st.session_state.sim_elec,
                "diet": st.session_state.sim_diet,
                "renew": st.session_state.sim_renew,
                "waste": st.session_state.sim_waste,
                "air": st.session_state.sim_air,
                "shop": st.session_state.sim_shop
            }
        }
        st.success("Scenario saved to session.")
with col_apply:
    if "saved_simulation" in st.session_state and st.button("Load Saved Scenario"):
        s = st.session_state["saved_simulation"]["sliders"]
        st.session_state.sim_car = s["car"]
        st.session_state.sim_elec = s["elec"]
        st.session_state.sim_diet = s["diet"]
        st.session_state.sim_renew = s["renew"]
        st.session_state.sim_waste = s["waste"]
        st.session_state.sim_air = s["air"]
        st.session_state.sim_shop = s["shop"]
        st.experimental_rerun()

st.markdown("---")
st.markdown("<div class='small-muted'>Tip: Use the sliders to experiment — the pie on the right updates live and the 'Estimated Green Score' shows the projected outcome.</div>", unsafe_allow_html=True)
