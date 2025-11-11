import streamlit as st
import plotly.graph_objects as go

def kpi_tiles(total_kg: float, energy_kg: float, travel_kg: float, food_kg: float):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total CO₂ (kg/mo)", f"{total_kg:.1f}")
    c2.metric("Energy", f"{energy_kg:.1f} kg")
    c3.metric("Travel", f"{travel_kg:.1f} kg")
    c4.metric("Food", f"{food_kg:.1f} kg")

def donut_breakdown(d: dict, title: str = ""):
    labels = list(d.keys()); values = [float(v) for v in d.values()]
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.58)])
    fig.update_traces(
        hoverinfo="label+percent",
        textinfo="value",
        textfont_size=14
    )
    fig.update_layout(margin=dict(l=10,r=10,b=10,t=40), title=title, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

def trend_line(points):
    xs = [p["x"] for p in points]; ys = [p["y"] for p in points]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", name="Monthly CO₂"))
    fig.update_layout(title="Predicted Trend (next 12 months)", margin=dict(l=10,r=10,b=10,t=40))
    st.plotly_chart(fig, use_container_width=True)

def gauge(score: int):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Green Score"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': '#45f1a0'},
               'steps': [
                   {'range': [0, 60], 'color': '#2a2f47'},
                   {'range': [60, 80], 'color': '#22324a'},
                   {'range': [80, 100], 'color': '#1c364d'}]}
    ))
    fig.update_layout(height=260, margin=dict(l=10,r=10,b=10,t=40))
    st.plotly_chart(fig, use_container_width=True)
