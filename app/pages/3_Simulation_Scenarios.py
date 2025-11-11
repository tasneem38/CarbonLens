import streamlit as st
from app.components.charts import donut_breakdown
from app.utils_local_calc import simulate_with_sliders

st.set_page_config(page_title="What-If Scenarios", page_icon="🕹️", layout="wide")
st.markdown('<div class="page-title">What-If Scenarios (Savings Preview)</div>', unsafe_allow_html=True)

base_inputs = None
if "last_result" in st.session_state:
    base_inputs = st.session_state["last_result"].get("inputs")
else:
    base_inputs = {"electricityKwh":180, "carKm":200, "busKm":120, "diet":"mixed"}

c1, c2, c3 = st.columns(3)
with c1:
    car_reduce = st.slider("Reduce car travel (%)", 0, 100, 20, 5)
with c2:
    elec_reduce = st.slider("Reduce electricity use (%)", 0, 100, 15, 5)
with c3:
    diet_shift = st.slider("Shift to low-carbon diet (%)", 0, 100, 25, 5)

before, after = simulate_with_sliders(base_inputs, car_reduce, elec_reduce, diet_shift)

st.markdown("### Before vs After (kg CO₂/month)")
colA, colB = st.columns(2)
with colA:
    donut_breakdown(before, title="Before")
with colB:
    donut_breakdown(after, title="After")

delta = sum(before.values()) - sum(after.values())
st.success(f"Estimated reduction: **{delta:.1f} kg CO₂ / month**")
