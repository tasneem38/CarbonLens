import streamlit as st
import requests
import os

st.set_page_config(page_title="Leaderboard & Badges", page_icon="🏅", layout="wide")
st.markdown('<div class="page-title">Leaderboard & Badges</div>', unsafe_allow_html=True)

API = os.getenv("CARBONLENS_API", "http://localhost:8000/api")

try:
    res = requests.get(f"{API}/leaderboard", timeout=5)
    data = res.json()
except:
    data = []

if not data:
    st.info("No leaderboard data yet. Run an analysis first!")
else:
    cols = st.columns(3)
    for i, s in enumerate(data[:3]):  # Top 3 only
        with cols[i]:
            st.markdown(f"""
            <div class="card badge-card">
              <div class="label">Top {i+1}</div>
              <div class="badge-title">{s['name']}</div>
              <div class="muted">Score</div>
              <div class="badge-score">{s['score']}</div>
            </div>
            """, unsafe_allow_html=True)
