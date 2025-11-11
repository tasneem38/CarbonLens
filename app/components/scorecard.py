import streamlit as st

def score_card(score: int):
    remark = "Excellent" if score >= 80 else "Good" if score >= 60 else "Needs Work"
    color  = "var(--success)" if score >= 80 else "var(--warning)" if score >= 60 else "var(--danger)"
    st.markdown(f"""
    <div class="card kpi">
      <div class="label">Realtime Green Score</div>
      <div class="score-bounce" style="color:{color}">{score}</div>
      <div class="muted">{remark} — higher is better</div>
    </div>
    """, unsafe_allow_html=True)
