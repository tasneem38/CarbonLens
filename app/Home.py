import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="CarbonLens — Personal CO₂ Tracker",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ✅ Inject CSS
st.markdown("""
<style>
/* Full-page background */
body, html, .main, .block-container, .appview-container {
    min-height: 100vh;
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)), url('https://images.unsplash.com/photo-1500530855697-b586d89ba3ee') center/cover no-repeat fixed !important;
    background-attachment: fixed !important;
}

/* Hero container - REDUCED HEIGHT */
.hero-container {
    min-height: 80vh; /* REDUCED from 100vh to 80vh */
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    margin: 0;
    padding: 0;
}

/* Titles and subtitles */
.title {
    font-size: 54px;
    font-weight: 800;
    color: #e0f0d9;
}

.subtitle {
    font-size: 18px;
    color: #c8d5ca;
    margin-bottom: 30px;
}

/* Button Styles */
.cta-buttons .btn {
    margin: 10px;
    padding: 12px 20px;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s;
    display: inline-block;
}
.btn.primary {
    background: #6de28d;
    color: #0b1120;
}
.btn.secondary { background: #22354a; color: white; }
.btn.ghost { border: 1px solid #dce3ea; color: white; }
.btn:hover { transform: translateY(-4px); }

/* Features Section - MINIMAL SPACING */
.features-section {
    text-align: center;
    padding: 20px 20px 60px 20px; /* REDUCED top padding */
    background: transparent !important;
    position: relative;
    z-index: 2;
}

/* Features section heading */
.features-section h2 {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 40px;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

/* Features grid layout - HORIZONTAL */
.features-grid {
    display: flex;
    gap: 28px;
    justify-content: center;
    align-items: stretch;
    flex-wrap: nowrap;
    padding: 20px;
    overflow-x: auto;
}

/* Feature cards - VISIBLE */
.feature-card {
    min-width: 280px;
    background: rgba(255, 255, 255, 0.25);
    border: 1px solid rgba(255,255,255,0.4);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 32px 24px;
    text-align: center;
    color: #ffffff;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    flex-shrink: 0;
}

/* Feature card hover effect */
.feature-card:hover {
    transform: translateY(-8px);
    background: rgba(255, 255, 255, 0.3);
    box-shadow: 0 12px 32px rgba(109, 226, 141, 0.5);
    border: 1px solid rgba(109, 226, 141, 0.6);
    transition: all 0.3s ease;
}

/* Feature card icon */
.feature-card .icon {
    font-size: 44px;
    margin-bottom: 12px;
    color: #6de28d;
}

/* Headings inside card */
.feature-card h4 {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 8px;
    color: #ffffff;
}

/* Paragraph inside card */
.feature-card p {
    font-size: 14px;
    color: #e8f5e9;
}
</style>
""", unsafe_allow_html=True)

# ✅ HERO SECTION
st.markdown("""
<div class="hero-container">
    <div class="hero-content">
        <h1 class="title">Track. Reduce. Inspire. 🌱</h1>
        <p class="subtitle">
            A dynamic way to understand your carbon footprint — powered by AI recommendations, 
            beautiful dashboards, and actionable simulations.
        </p>
        <div class="cta-buttons">
            <a class="btn primary" href="app/pages/1_Analyze_Footprint.py" target="_self">🔍 Start Footprint Analysis</a>
            <a class="btn secondary" href="app/pages/3_Simulation_Scenarios.py" target="_self">🛠 Try What-If Simulator</a>
            <a class="btn ghost" href="app/pages/4_Leaderboard_and_Badges.py" target="_self">🏅 Leaderboard</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ✅ FEATURES SECTION - APPEARS RIGHT AFTER
st.markdown("""
<div class="features-section">
    <h2>Why CarbonLens?</h2>
    <div class="features-grid">
        <div class="feature-card">
            <div class="icon">🤖</div>
            <h4>AI-Driven Suggestions</h4>
            <p>Smart tips tailored to your lifestyle and habits.</p>
        </div>
        <div class="feature-card">
            <div class="icon">📊</div>
            <h4>Live Carbon Dashboard</h4>
            <p>Instant visualization across energy, travel, and food.</p>
        </div>
        <div class="feature-card">
            <div class="icon">🎮</div>
            <h4>Gamified Challenges</h4>
            <p>Earn badges, climb the leaderboard, and inspire others.</p>
        </div>
        <div class="feature-card">
            <div class="icon">🧪</div>
            <h4>What-If Simulations</h4>
            <p>See CO₂ savings before lifestyle changes.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)