import streamlit as st
import os
import requests
import random
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Recommendations - CarbonLens", page_icon="🤖", layout="wide")
st.markdown('<div class="page-title">🤖 AI Recommendations</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Get personalized carbon reduction strategies — quick, practical, and ranked by impact.</div>', unsafe_allow_html=True)

# -----------------------
# CSS Styles
# -----------------------
st.markdown("""
<style>
:root{
    --bg: #0f172a;
    --card-bg: rgba(30,41,59,0.85);
    --muted: #94a3b8;
    --accent: #00d4aa;
    --accent2: #6c63ff;
    --glass-border: rgba(255,255,255,0.06);
}
body, html, .main, .block-container {
    background: linear-gradient(135deg,var(--bg), #121827) !important;
    color: #e6eef6;
    font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    font-size: 16px;
}
/* Title & subtitle styling */
.page-title { 
    font-size: 2.8rem;
    font-weight: 800; 
    margin-bottom: 0.5rem; 
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}
.subtitle { 
    color: var(--muted); 
    margin-bottom: 1.5rem; 
    text-align: center;
    font-size: 1.3rem;
}
/* Metrics grid */
.metrics-container {
    display: flex;
    justify-content: space-around;
    margin-bottom: 30px;
}
.metric {
    background: var(--card-bg);
    padding: 20px 30px;
    border-radius: 12px;
    text-align: center;
    width: 20%;
    border: 1px solid rgba(255,255,255,0.1);
}
.metric h2 {
    margin: 0;
    font-size: 2.1rem;
    font-weight: 700;
    color: #e6fff7;
}
.metric p {
    margin: 5px 0 0;
    color: var(--muted);
    font-size: 1rem;
}
/* Progress bar section */
.progress-section {
    background: rgba(30,41,59,0.8);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 25px;
    margin-bottom: 30px;
}
/* Feature cards layout */
.features-grid {
    display: flex;
    flex-direction: column;
    gap: 24px;
    width: 100%;
}

/* Four cards - first row */
.card-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

/* Three cards - second row */
.card-row-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

/* Individual card styling */
.feature-card {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 24px 24px 28px 24px;
    border: 1px solid var(--glass-border);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    display: flex;
    flex-direction: column;
    height: 380px;
    transition: all 0.3s ease;
}
.feature-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    border-color: rgba(0,212,170,0.2);
}

/* Badges */
.card-badges {
    display: flex;
    gap: 8px;
    margin-bottom: 18px;
    flex-wrap: wrap;
}
.badge {
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    white-space: nowrap;
}
.badge-cat {
    background: rgba(0,212,170,0.15);
    color: var(--accent);
    border: 1px solid rgba(0,212,170,0.3);
}
.badge-diff {
    background: rgba(108,99,255,0.15);
    color: var(--accent2);
    border: 1px solid rgba(108,99,255,0.3);
}
.badge-impact {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: white;
    border: none;
}

/* Card title and description */
.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f7fbfa;
    margin-bottom: 14px;
    line-height: 1.3;
}
.card-desc {
    font-size: 0.95rem;
    color: var(--muted);
    flex-grow: 1;
    margin-bottom: 20px;
    line-height: 1.5;
}

/* Card metrics section */
.card-metrics {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
}
.metric-item {
    background: rgba(255,255,255,0.05);
    padding: 14px 12px;
    border-radius: 10px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}
.metric-label {
    font-size: 0.8rem;
    color: var(--muted);
    margin-bottom: 6px;
}
.metric-value {
    font-weight: 700;
    color: #e6fff7;
    font-size: 1rem;
}

/* Checkbox spacing for implemented actions */
.checkbox-wrapper {
    margin-top: 20px;
}
/* expander styling for steps and details */
.stExpander > div > div {
    background: var(--card-bg) !important;
    border-radius: 12px !important;
    color: var(--muted) !important;
    font-size: 0.9rem !important;
}

/* Responsive Grids on smaller screens */
@media (max-width: 1024px) {
    .card-row {
        grid-template-columns: repeat(2, 1fr);
    }
    .card-row-3 {
        grid-template-columns: repeat(2, 1fr);
    }
}
@media (max-width: 600px) {
    .card-row, .card-row-3 {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# --- Sample data ---
totals = {"total": 580, "energy": 220, "travel": 180, "food": 120, "goods": 60}
score = 65
profile = "Urban Commuter"

# --- Sample recommendation data ---
recommendations = [
    {
        "id": "led_lighting",
        "category": "⚡ Energy",
        "difficulty": "Easy",
        "impact_level": "Medium Impact",
        "title": "Switch to LED Lighting",
        "description": "Replace incandescent bulbs with energy-efficient LEDs throughout your home.",
        "potential_savings": 25,
        "cost": "Low",
        "timeline": "1 week",
        "steps": [
            "Audit current bulbs",
            "Purchase LED replacements",
            "Replace bulbs systematically"
        ],
        "icon": "💡"
    },
    {
        "id": "smart_thermostat",
        "category": "⚡ Energy",
        "difficulty": "Medium",
        "impact_level": "High Impact",
        "title": "Install Smart Thermostat",
        "description": "Optimize heating & cooling automatically based on your schedule.",
        "potential_savings": 40,
        "cost": "Medium",
        "timeline": "2 weeks",
        "steps": [
            "Research models",
            "Schedule installation",
            "Configure settings"
        ],
        "icon": "🌡️"
    },
    {
        "id": "unplug_devices",
        "category": "⚡ Energy",
        "difficulty": "Easy",
        "impact_level": "Low Impact",
        "title": "Unplug Idle Electronics",
        "description": "Reduce phantom power from devices on standby.",
        "potential_savings": 12,
        "cost": "None",
        "timeline": "Immediate",
        "steps": [
            "Identify standby devices",
            "Use power strips",
            "Switch off when idle"
        ],
        "icon": "🔌"
    },
    {
        "id": "energy_audit",
        "category": "⚡ Energy",
        "difficulty": "Medium",
        "impact_level": "High Impact",
        "title": "Home Energy Audit",
        "description": "Professional assessment to identify energy waste areas.",
        "potential_savings": 35,
        "cost": "Medium",
        "timeline": "2 weeks",
        "steps": [
            "Schedule audit",
            "Implement recommendations",
            "Monitor savings"
        ],
        "icon": "📊"
    },
    {
        "id": "public_transport",
        "category": "🚗 Travel",
        "difficulty": "Medium",
        "impact_level": "High Impact",
        "title": "Use Public Transport",
        "description": "Replace car trips with bus/train options where feasible.",
        "potential_savings": 40,
        "cost": "Low",
        "timeline": "Immediate",
        "steps": [
            "Research routes",
            "Get transit pass",
            "Plan commutes"
        ],
        "icon": "🚌"
    },
    {
        "id": "carpooling",
        "category": "🚗 Travel",
        "difficulty": "Easy",
        "impact_level": "Medium Impact",
        "title": "Start Carpooling",
        "description": "Share commutes with colleagues or neighbors.",
        "potential_savings": 27,
        "cost": "None",
        "timeline": "1 week",
        "steps": [
            "Find partners",
            "Set schedule",
            "Share costs"
        ],
        "icon": "👥"
    },
    {
        "id": "eco_driving",
        "category": "🚗 Travel",
        "difficulty": "Easy",
        "impact_level": "Medium Impact",
        "title": "Eco-Driving Habits",
        "description": "Adopt fuel-efficient driving techniques.",
        "potential_savings": 20,
        "cost": "None",
        "timeline": "Immediate",
        "steps": [
            "Smooth acceleration",
            "Proper tire pressure",
            "Reduce idling"
        ],
        "icon": "🚗"
    }
]

# Initialize session state
if "implemented_recommendations" not in st.session_state:
    st.session_state.implemented_recommendations = set()
if "show_steps" not in st.session_state:
    st.session_state.show_steps = {}
if "show_details" not in st.session_state:
    st.session_state.show_details = {}

# --- Display the actual footprint overview (metrics) ---
st.markdown("### 📊 Your Carbon Overview")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Green Score", f"{score}/100")
with col2:
    st.metric("Monthly CO₂", f"{totals['total']} kg")
with col3:
    highest_impact = max({k: v for k, v in totals.items() if k != "total"}, key=totals.get)
    st.metric("Highest Impact", highest_impact.title())
with col4:
    progress_count = len(st.session_state.implemented_recommendations)
    st.metric("Implemented Actions", f"{progress_count}/{len(recommendations)}")

# --- Progress section ---
st.markdown('<div class="progress-section">', unsafe_allow_html=True)
if progress_count > 0:
    total_potential = sum(r["potential_savings"] for r in recommendations)
    achieved_savings = sum(r["potential_savings"] for r in recommendations if r["id"] in st.session_state.implemented_recommendations)
    progress_percent = (progress_count / len(recommendations)) * 100
    savings_percent = (achieved_savings / total_potential) * 100 if total_potential else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Actions Completed**")
        st.metric("", f"{progress_count} / {len(recommendations)} ({progress_percent:.1f}%)")
        st.progress(progress_percent / 100)
    with col2:
        st.markdown("**CO₂ Savings Achieved**")
        st.metric("", f"{int(achieved_savings)} kg / {int(total_potential)} kg ({savings_percent:.1f}%)")
        st.progress(min(1.0, savings_percent / 100))
else:
    st.info("🌱 Start by marking recommendations as implemented to track your progress.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# --- Feature cards with recommendations ---
st.markdown('<div class="features-grid">', unsafe_allow_html=True)

# Four cards in first row
st.markdown('<div class="card-row">', unsafe_allow_html=True)
for rec in recommendations[:4]:
    is_implemented = rec["id"] in st.session_state.implemented_recommendations
    card_html = f'''
    <div class="feature-card">
        <div class="card-badges">
            <span class="badge badge-cat">{rec["category"]}</span>
            <span class="badge badge-diff">{rec["difficulty"]}</span>
            <span class="badge badge-impact">{rec["impact_level"]}</span>
        </div>
        <div class="card-title">{rec["title"]}</div>
        <div class="card-desc">{rec["description"]}</div>
        <div class="card-metrics">
            <div class="metric-item">
                <div class="metric-label">CO₂ Savings</div>
                <div class="metric-value">{int(rec["potential_savings"])} kg/mo</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Cost</div>
                <div class="metric-value">{rec.get("cost", "Varies")}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Timeline</div>
                <div class="metric-value">{rec.get("timeline", "Varies")}</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(card_html, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Steps", key=f"steps_{rec['id']}", use_container_width=True):
            st.session_state.show_steps[rec["id"]] = True
    with col2:
        if st.button("💡 Details", key=f"details_{rec['id']}", use_container_width=True):
            st.session_state.show_details[rec["id"]] = True
    checked = st.checkbox(
        "✅ Mark as implemented",
        value=is_implemented,
        key=f"impl_{rec['id']}",
        help="Mark recommendation as implemented"
    )
    if checked:
        st.session_state.implemented_recommendations.add(rec["id"])
    else:
        st.session_state.implemented_recommendations.discard(rec["id"])

    if st.session_state.show_steps.get(rec["id"]):
        with st.expander("Implementation Steps", expanded=True):
            for step in rec.get("steps", []):
                st.markdown(f"- {step}")
        st.session_state.show_steps[rec["id"]] = False

    if st.session_state.show_details.get(rec["id"]):
        with st.expander("More Information", expanded=True):
            st.markdown(f"**Category:** {rec['category']}")
            st.markdown(f"**Difficulty:** {rec['difficulty']}")
            st.markdown(f"**Impact:** {rec['impact_level']}")
            st.markdown(f"**Potential Savings:** {int(rec['potential_savings'])} kg CO₂/month")
            st.markdown(f"**Timeline:** {rec.get('timeline', 'Varies')}")
            st.markdown(f"**Cost:** {rec.get('cost', 'Varies')}")
        st.session_state.show_details[rec["id"]] = False
st.markdown('</div>', unsafe_allow_html=True)

# Three cards in second row
st.markdown('<div class="card-row-3">', unsafe_allow_html=True)
for rec in recommendations[4:7]:
    is_implemented = rec["id"] in st.session_state.implemented_recommendations
    card_html = f'''
    <div class="feature-card">
        <div class="card-badges">
            <span class="badge badge-cat">{rec["category"]}</span>
            <span class="badge badge-diff">{rec["difficulty"]}</span>
            <span class="badge badge-impact">{rec["impact_level"]}</span>
        </div>
        <div class="card-title">{rec["title"]}</div>
        <div class="card-desc">{rec["description"]}</div>
        <div class="card-metrics">
            <div class="metric-item">
                <div class="metric-label">CO₂ Savings</div>
                <div class="metric-value">{int(rec["potential_savings"])} kg/mo</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Cost</div>
                <div class="metric-value">{rec.get("cost", "Varies")}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Timeline</div>
                <div class="metric-value">{rec.get("timeline", "Varies")}</div>
            </div>
        </div>
    </div>
    '''
    st.markdown(card_html, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Steps", key=f"steps_{rec['id']}_2", use_container_width=True):
            st.session_state.show_steps[rec["id"]] = True
    with col2:
        if st.button("💡 Details", key=f"details_{rec['id']}_2", use_container_width=True):
            st.session_state.show_details[rec["id"]] = True
    checked = st.checkbox(
        "✅ Mark as implemented",
        value=is_implemented,
        key=f"impl_{rec['id']}_2",
        help="Mark recommendation as implemented"
    )
    if checked:
        st.session_state.implemented_recommendations.add(rec["id"])
    else:
        st.session_state.implemented_recommendations.discard(rec["id"])
    
    if st.session_state.show_steps.get(rec["id"]):
        with st.expander("Implementation Steps", expanded=True):
            for step in rec.get("steps", []):
                st.markdown(f"- {step}")
        st.session_state.show_steps[rec["id"]] = False
    if st.session_state.show_details.get(rec["id"]):
        with st.expander("More Information", expanded=True):
            st.markdown(f"**Category:** {rec['category']}")
            st.markdown(f"**Difficulty:** {rec['difficulty']}")
            st.markdown(f"**Impact:** {rec['impact_level']}")
            st.markdown(f"**Potential Savings:** {int(rec['potential_savings'])} kg CO₂/month")
            st.markdown(f"**Timeline:** {rec.get('timeline', 'Varies')}")
            st.markdown(f"**Cost:** {rec.get('cost', 'Varies')}")
        st.session_state.show_details[rec["id"]] = False
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# Chatbot Section - FIXED VERSION
# -----------------------
st.markdown("### 💬 Carbon Reduction Assistant")

st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Initialize and validate chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Clean up any invalid messages in chat history
st.session_state.chat_history = [
    msg for msg in st.session_state.chat_history 
    if isinstance(msg, dict) and "role" in msg and "content" in msg
]

# Display chat history with proper error handling
for i, message in enumerate(st.session_state.chat_history):
    try:
        role = message.get("role", "")
        content = message.get("content", "")
        
        if not content:  # Skip empty messages
            continue
            
        # Ensure content is a string
        safe_content = str(content).replace('"', '&quot;').replace("'", "&#39;")
        
        if role == "user":
            st.markdown(
                f'<div class="chat-message user-message"><strong>You:</strong> {safe_content}</div>', 
                unsafe_allow_html=True
            )
        elif role == "assistant":
            st.markdown(
                f'<div class="chat-message bot-message"><strong>Assistant:</strong> {safe_content}</div>', 
                unsafe_allow_html=True
            )
    except Exception as e:
        # Skip problematic messages
        continue

# Chat input with a form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Ask me about carbon reduction strategies:", 
        key="chat_input", 
        placeholder="e.g., What are the easiest ways to reduce my emissions?"
    )
    submit_button = st.form_submit_button("Send", use_container_width=True)

if submit_button and user_input.strip():
    # Add user message to history with proper structure
    st.session_state.chat_history.append({
        "role": "user", 
        "content": user_input.strip()
    })
    
    # Generate bot response with error handling
    try:
        bot_response = generate_conversational_response(
            user_input.strip(), 
            totals, 
            score, 
            profile, 
            st.session_state.chat_history
        )
        
        # Ensure bot response is a valid string
        if not bot_response or not isinstance(bot_response, str):
            bot_response = "I'm here to help with carbon reduction strategies. What would you like to know?"
        
        # Clean the response
        bot_response = str(bot_response).strip()
        
        # Add bot response to history with proper structure
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": bot_response
        })
        
    except Exception as e:
        error_response = "I'm having trouble responding right now. Please try asking about specific carbon reduction strategies like LED lighting, public transport, or plant-based diets."
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": error_response
        })
    
    # Rerun to update the display
    st.rerun()

# Clear chat button
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
