import streamlit as st

def lifestyle_form(demo_select: str) -> dict:
    presets = {
        "Urban Commuter": dict(electricityKwh=180, carKm=260, busKm=40, diet="mixed"),
        "Student Hostel": dict(electricityKwh=120, carKm=20,  busKm=160, diet="veg"),
        "Frequent Flyer":  dict(electricityKwh=260, carKm=180, busKm=80,  diet="nonveg"),
    }
    if demo_select in presets:
        st.success(f"Loaded demo: {demo_select}")
        values = presets[demo_select].copy()
    else:
        values = dict(electricityKwh=180, carKm=200, busKm=120, diet="mixed")

    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            values["electricityKwh"] = st.number_input("Monthly electricity (kWh)", 0, 99999, values["electricityKwh"])
        with c2:
            values["carKm"] = st.number_input("Car travel (km/month)", 0, 100000, values["carKm"])
        with c3:
            values["busKm"] = st.number_input("Bus/Metro travel (km/month)", 0, 100000, values["busKm"])

        diet = st.selectbox("Diet type", ["veg", "mixed", "nonveg"], index=["veg","mixed","nonveg"].index(values["diet"]))
        values["diet"] = diet

    return values
