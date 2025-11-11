import os
import requests
import streamlit as st
import time
from app.components.toasts import toast_warn, toast_success
from app.components.charts import kpi_tiles

st.set_page_config(page_title="AI Carbon Coach", page_icon="🤖", layout="wide")

# Modern CSS Styling
st.markdown("""
<style>
.page-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 10px;
    padding: 20px;
}

.chat-container {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #e0e0e0;
    border-radius: 16px;
    padding: 20px;
    margin: 15px 0;
    max-height: 500px;
    overflow-y: auto;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.user-message {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    margin-left: 50px;
    border: 1px solid rgba(255, 255, 255, 0.3);
    max-width: 80%;
}

.ai-message {
    background: #f8f9fa;
    color: #333333;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    margin-right: 50px;
    border: 1px solid #e0e0e0;
    max-width: 80%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.typing-indicator {
    display: inline-block;
    margin-left: 8px;
}

.typing-dot {
    height: 6px;
    width: 6px;
    background-color: #6366f1;
    border-radius: 50%;
    display: inline-block;
    margin: 0 1px;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

.reco-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 12px;
    margin: 8px 0;
    border-left: 4px solid;
    transition: all 0.3s ease;
    color: #333333;
}

.reco-card:hover {
    transform: translateX(5px);
    background: #e9ecef;
}

.reco-energy { border-left-color: #f59e0b; }
.reco-travel { border-left-color: #06b6d4; }
.reco-food { border-left-color: #10b981; }
.reco-shopping { border-left-color: #8b5cf6; }
.reco-general { border-left-color: #6366f1; }

.area-badge {
    background: #6366f1;
    color: white;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 6px;
}

.impact-badge {
    background: rgba(16, 185, 129, 0.2);
    color: #10b981;
    padding: 3px 8px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 600;
    margin-right: 6px;
}

.confidence-badge {
    background: rgba(99, 102, 241, 0.2);
    color: #6366f1;
    padding: 3px 8px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">💬 AI Carbon Coach</div>', unsafe_allow_html=True)

API = "http://localhost:8000/api"

# Initialize chat session
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "ai_thinking" not in st.session_state:
    st.session_state.ai_thinking = False

# Check if we have footprint data
if "last_result" not in st.session_state:
    st.error("🚫 No carbon footprint data found!")
    st.info("Please complete your footprint analysis first on the 'Analyze Footprint' page to get personalized recommendations.")
    st.markdown("[Go to Analyze Footprint](/Analyze_Footprint)")
    st.stop()

# Get the last result
last_result = st.session_state["last_result"]
totals = last_result["totals"]
inputs = last_result.get("inputs", {})

# Header with user's footprint summary
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown("### Your Personal Carbon Coach")
    st.caption("Powered by Gemini AI - Get personalized carbon reduction advice")
with col2:
    st.metric("Total Footprint", f"{totals['total']} kg CO₂")
with col3:
    st.metric("Green Score", f"{last_result['score']}/100")

# KPI Overview
st.markdown("---")
st.markdown("### 📊 Your Current Footprint")
kpi_tiles(
    total_kg=totals["total"],
    energy_kg=totals["energy"],
    travel_kg=totals["travel"],
    food_kg=totals["food"]
)

# Initialize chat with AI recommendations if first time
if not st.session_state.chat_messages:
    # Add welcome message
    welcome_message = f"""👋 **Hello! I'm your AI Carbon Coach, powered by Google Gemini.**

I've analyzed your carbon footprint of **{totals['total']} kg CO₂/month** and I'm here to provide personalized, AI-powered recommendations to help you reduce it!

**Your emission breakdown:**
• **Energy**: {totals['energy']} kg CO₂ ({round((totals['energy']/totals['total'])*100)}%)
• **Travel**: {totals['travel']} kg CO₂ ({round((totals['travel']/totals['total'])*100)}%)  
• **Food**: {totals['food']} kg CO₂ ({round((totals['food']/totals['total'])*100)}%)

I can provide specific, actionable advice tailored to your lifestyle and answer any questions about carbon reduction!

**What would you like to know about reducing your carbon footprint?**"""
    
    st.session_state.chat_messages.append({
        "role": "ai",
        "content": welcome_message,
        "timestamp": time.time()
    })

# Chat Interface
st.markdown("---")
st.markdown("### 💬 AI Conversation")

# Chat container
with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        if message["role"] == "user":
            st.markdown(f'''
            <div style="display: flex; align-items: end; margin-bottom: 12px; justify-content: flex-end;">
                <div class="user-message">
                    {message["content"]}
                </div>
                <div style="width: 35px; height: 35px; border-radius: 50%; background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); display: flex; align-items: center; justify-content: center; margin-left: 10px; flex-shrink: 0;">
                    <span style="color: white; font-size: 12px; font-weight: bold;">You</span>
                </div>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div style="display: flex; align-items: start; margin-bottom: 12px;">
                <div style="width: 35px; height: 35px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); display: flex; align-items: center; justify-content: center; margin-right: 10px; flex-shrink: 0;">
                    <span style="color: white; font-size: 12px; font-weight: bold;">AI</span>
                </div>
                <div class="ai-message">
                    {message["content"]}
                </div>
            </div>
            ''', unsafe_allow_html=True)
    
    # Show typing indicator if AI is thinking
    if st.session_state.ai_thinking:
        st.markdown(f'''
        <div style="display: flex; align-items: start; margin-bottom: 12px;">
            <div style="width: 35px; height: 35px; border-radius: 50%; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); display: flex; align-items: center; justify-content: center; margin-right: 10px; flex-shrink: 0;">
                <span style="color: white; font-size: 12px; font-weight: bold;">AI</span>
            </div>
            <div class="ai-message">
                Gemini AI is thinking
                <span class="typing-indicator">
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                    <span class="typing-dot"></span>
                </span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Quick questions
st.markdown("#### 💡 Quick Questions")
quick_cols = st.columns(4)
quick_questions = [
    "What are my biggest emission sources?",
    "Give me energy-saving tips",
    "How to reduce travel emissions?",
    "Best diet changes?"
]

for i, question in enumerate(quick_questions):
    with quick_cols[i % 4]:
        if st.button(question, use_container_width=True, key=f"quick_{i}"):
            st.session_state.chat_messages.append({
                "role": "user", 
                "content": question,
                "timestamp": time.time()
            })
            st.session_state.ai_thinking = True
            st.rerun()

# Chat input
st.markdown("---")
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "💭 Ask me anything about reducing your carbon footprint...",
        placeholder="e.g., How can I reduce my electricity bill? Best ways to cut travel emissions? Sustainable eating tips?",
        key="chat_input"
    )
    
    col1, col2 = st.columns([4, 1])
    with col2:
        submit = st.form_submit_button("Send ➤", use_container_width=True)

# Process user input
if submit and user_input.strip():
    # Add user message to chat
    st.session_state.chat_messages.append({
        "role": "user",
        "content": user_input.strip(),
        "timestamp": time.time()
    })
    
    st.session_state.ai_thinking = True
    st.rerun()

# AI Response Generation (after rerun)
if st.session_state.ai_thinking:
    # Get the last user message
    last_user_message = None
    for message in reversed(st.session_state.chat_messages):
        if message["role"] == "user":
            last_user_message = message["content"]
            break
    
    if last_user_message:
        try:
            # Prepare enhanced payload for AI
            enhanced_payload = {
                **inputs,
                "energy_kg": totals["energy"],
                "travel_kg": totals["travel"],
                "food_kg": totals["food"],
                "goods_kg": totals.get("goods", 0),
                "user_question": last_user_message
            }
            
            # Call AI chat API
            r = requests.post(f"{API}/reco/chat", json=enhanced_payload, timeout=30)
            
            if r.status_code == 200:
                response_data = r.json()
                ai_response = response_data.get("response", "I'm here to help you reduce your carbon footprint!")
                toast_success("✅ Gemini AI response generated!")
            else:
                raise Exception(f"API returned {r.status_code}: {r.text}")
            
            # Add AI response to chat
            st.session_state.chat_messages.append({
                "role": "ai",
                "content": ai_response,
                "timestamp": time.time()
            })
            
        except Exception as e:
            # Error response
            error_msg = f"I apologize, but I'm having trouble connecting to the AI service right now. Please try again in a moment. (Error: {str(e)})"
            st.session_state.chat_messages.append({
                "role": "ai",
                "content": error_msg,
                "timestamp": time.time()
            })
            toast_warn("⚠️ Temporary AI service issue")
        
        finally:
            st.session_state.ai_thinking = False
            st.rerun()

# AI Recommendations Section
st.markdown("---")
st.markdown("### 🎯 AI-Generated Action Plan")

with st.spinner('🤖 Gemini AI is generating personalized recommendations...'):
    try:
        # Prepare payload for AI recommendations
        reco_payload = {
            **inputs,
            "energy_kg": totals["energy"],
            "travel_kg": totals["travel"], 
            "food_kg": totals["food"],
            "goods_kg": totals.get("goods", 0)
        }
        
        r = requests.post(f"{API}/reco/generate", json=reco_payload, timeout=30)
        if r.status_code == 200:
            tips_data = r.json()
            tips = tips_data.get("tips", [])
            st.success("✅ AI recommendations generated successfully!")
        else:
            raise Exception(f"API returned {r.status_code}")
            
    except Exception as e:
        st.error(f"❌ Could not generate AI recommendations: {str(e)}")
        st.info("Please check that your backend is running and GEMINI_API_KEY is set correctly.")
        tips = []

# Display AI recommendations
if tips:
    st.markdown(f"**Gemini AI found {len(tips)} personalized recommendations for you:**")
    
    for i, tip in enumerate(tips):
        area = tip.get('area', 'General').lower()
        impact = tip.get('impact_kg_month', 0)
        confidence = tip.get('confidence', 0.8)
        
        card_class = f"reco-card reco-{area}"
        
        st.markdown(f"""
        <div class="{card_class}">
            <div class="area-badge">🔮 {tip.get('area', 'General')}</div>
            <p style="margin: 8px 0; font-weight: 500;">{tip.get('text', '')}</p>
            <div style="display: flex; gap: 10px; margin-top: 10px;">
                <span class="impact-badge">🌱 Saves {impact} kg CO₂/month</span>
                <span class="confidence-badge">🎯 {int(confidence*100)}% confidence</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Clear chat button
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.ai_thinking = False
        st.rerun()

# Environment setup reminder
if not os.getenv("GEMINI_API_KEY"):
    st.markdown("---")
    st.warning("⚠️ **Setup Required**: To enable AI features, set your `GEMINI_API_KEY` environment variable in the backend.")
