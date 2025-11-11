import streamlit as st
import requests
import os

st.set_page_config(page_title="Leaderboard & Badges", page_icon="🏆", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
.page-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, #45f1a0, #37b3f5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}
.subtitle {
    text-align: center;
    color: #a9b3c7;
    margin-bottom: 50px;
    font-size: 18px;
}
.card {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 18px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 40px rgba(55, 179, 245, 0.25);
}
.badge-rank {
    font-size: 20px;
    font-weight: 700;
    color: #45f1a0;
}
.badge-title {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}
.badge-score {
    font-size: 40px;
    font-weight: 900;
    background: linear-gradient(135deg, #37b3f5, #45f1a0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.trophy {
    font-size: 48px;
    margin-bottom: 10px;
}
.top1 { color: gold; }
.top2 { color: silver; }
.top3 { color: #cd7f32; }
</style>
""", unsafe_allow_html=True)

# --- Page Header ---
st.markdown('<div class="page-title">🏆 CarbonLens Leaderboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Anonymous users ranked by Green Score 🌿</div>', unsafe_allow_html=True)

API = os.getenv("CARBONLENS_API", "http://localhost:8000/api")

try:
    res = requests.get(f"{API}/leaderboard", timeout=5)
    data = res.json()
except Exception as e:
    st.error(f"⚠️ Could not fetch leaderboard data — {e}")
    data = []

if not data:
    st.info("No leaderboard data yet. Run an analysis first!")
else:
    trophies = ["🥇", "🥈", "🥉"]
    cols = st.columns(3)

    for i, entry in enumerate(data[:3]):
        with cols[i]:
            st.markdown(f"""
            <div class="card">
                <div class="trophy {'top'+str(i+1)}">{trophies[i]}</div>
                <div class="badge-rank">Rank {i+1}</div>
                <div class="badge-title">{entry['name']}</div>
                <div class="muted">Green Score</div>
                <div class="badge-score">{entry['score']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🌱 Full Leaderboard")
    for i, entry in enumerate(data[3:], start=4):
        st.markdown(f"""
        <div class="card" style="margin-bottom:10px;">
            <b>#{i} {entry['name']}</b> — 
            <span style="color:#45f1a0;font-weight:700;">{entry['score']}</span> pts
        </div>
        """, unsafe_allow_html=True)
