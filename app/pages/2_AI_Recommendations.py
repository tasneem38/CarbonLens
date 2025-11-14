import streamlit as st
import os
import requests
from dotenv import load_dotenv
import random
import streamlit.components.v1 as components
import json

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Recommendations - CarbonLens", page_icon="🤖", layout="wide")

# ✅ THEME & STYLING
st.markdown("""
<style>
body, html, .main, .block-container, .appview-container {
    min-height: 100vh;
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    overflow-y: auto;
}

/* Color Palette */
:root {
    --primary: #00d4aa;
    --secondary: #6c63ff;
    --accent: #ff6b6b;
    --card-bg: rgba(30, 41, 59, 0.8);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
}

/* Title Styling */
.page-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
    padding: 2rem 1rem 1rem 1rem;
}

.subtitle {
    text-align: center;
    color: var(--text-secondary);
    margin-bottom: 3rem;
}

/* Feature Card Styling */
.feature-card {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.1);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    border-color: rgba(0, 212, 170, 0.3);
}

.metric {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
    transition: transform 0.2s ease;
}

.metric:hover {
    transform: translateY(-2px);
}

/* Badge Styling */
.category-badge {
    background: rgba(0, 212, 170, 0.2);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8em;
    color: #00d4aa;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 10px;
}

.difficulty-badge {
    background: rgba(108, 99, 255, 0.2);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8em;
    color: #6c63ff;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 10px;
}

.impact-badge {
    background: linear-gradient(135deg, #00d4aa, #6c63ff);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8em;
    color: white;
    font-weight: 600;
    display: inline-block;
    margin-bottom: 10px;
}

/* Action Buttons */
.action-buttons {
    display: flex;
    gap: 10px;
    margin-top: 15px;
    justify-content: center;
}

.emoji-button {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    font-size: 1.2em;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.emoji-button:hover {
    background: rgba(0, 212, 170, 0.3);
    transform: scale(1.1);
}

.implemented-checkbox {
    margin-top: 15px;
    padding: 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
}

/* Chat Widget Styles */
#chatButton {
    position: fixed !important;
    bottom: 25px !important;
    right: 25px !important;
    width: 70px !important;
    height: 70px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #00d4aa, #6c63ff) !important;
    box-shadow: 0 0 25px rgba(0, 212, 170, 0.6) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    z-index: 999999 !important;
    transition: all 0.3s ease !important;
    animation: pulse 2s infinite !important;
}

#chatButton:hover {
    transform: scale(1.08) !important;
    box-shadow: 0 0 35px rgba(0, 212, 170, 0.8) !important;
}

@keyframes pulse {
    0% { box-shadow: 0 0 15px rgba(0, 212, 170, 0.5); }
    50% { box-shadow: 0 0 30px rgba(0, 212, 170, 0.7); }
    100% { box-shadow: 0 0 15px rgba(0, 212, 170, 0.5); }
}

/* Ensure Streamlit's iframe doesn't block */
iframe[title="streamlitChatWidget"] {
    position: fixed !important;
    bottom: 0 !important;
    right: 0 !important;
    width: 1px !important;
    height: 1px !important;
    background: transparent !important;
    pointer-events: none !important;
    z-index: 999998 !important;
}
</style>
""", unsafe_allow_html=True)

# ✅ HEADER
st.markdown('<div class="page-title">🤖 AI Recommendations</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Get personalized carbon reduction strategies and chat with our AI assistant</div>', unsafe_allow_html=True)

# ✅ FUNCTIONS
def validate_environment():
    """Validate that required environment variables are available"""
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    if not api_key:
        st.warning("🔑 HuggingFace API key not found. Chat features will use fallback responses.")
        return False
    return True

def generate_dynamic_recommendations(totals, score, profile):
    """Generate personalized carbon reduction recommendations"""
    recs = []
    
    # Energy recommendations
    if totals.get('energy', 0) > 200:
        recs.extend([
            {
                'id': 'led_lighting',
                'category': '⚡ Energy',
                'difficulty': 'Easy',
                'impact_level': 'Medium',
                'title': 'Switch to LED Lighting',
                'description': 'Replace incandescent bulbs with energy-efficient LEDs throughout your home.',
                'potential_savings': 15,
                'cost': 'Low',
                'timeline': '1 week',
                'steps': ['Identify current bulb types', 'Purchase LED replacements', 'Replace bulbs gradually'],
                'icon': '💡'
            },
            {
                'id': 'smart_thermostat',
                'category': '⚡ Energy',
                'difficulty': 'Medium',
                'impact_level': 'High',
                'title': 'Install Smart Thermostat',
                'description': 'Optimize heating and cooling automatically based on your schedule.',
                'potential_savings': 30,
                'cost': 'Medium',
                'timeline': '2 weeks',
                'steps': ['Research compatible models', 'Schedule installation', 'Configure temperature schedules'],
                'icon': '🌡️'
            },
            {
                'id': 'unplug_devices',
                'category': '⚡ Energy',
                'difficulty': 'Easy',
                'impact_level': 'Low',
                'title': 'Unplug Idle Electronics',
                'description': 'Reduce phantom power consumption from devices on standby.',
                'potential_savings': 8,
                'cost': 'None',
                'timeline': 'Immediate',
                'steps': ['Identify energy vampires', 'Use power strips', 'Make it a daily habit'],
                'icon': '🔌'
            }
        ])
    
    # Travel recommendations
    if totals.get('travel', 0) > 150:
        recs.extend([
            {
                'id': 'public_transport',
                'category': '🚗 Travel',
                'difficulty': 'Medium',
                'impact_level': 'High',
                'title': 'Use Public Transportation',
                'description': 'Replace 3 car trips per week with public transport options.',
                'potential_savings': 45,
                'cost': 'Low',
                'timeline': 'Immediate',
                'steps': ['Research local routes', 'Get transit pass', 'Plan weekly schedule'],
                'icon': '🚌'
            },
            {
                'id': 'carpooling',
                'category': '🚗 Travel',
                'difficulty': 'Easy',
                'impact_level': 'Medium',
                'title': 'Start Carpooling',
                'description': 'Share rides with colleagues or neighbors for regular commutes.',
                'potential_savings': 25,
                'cost': 'None',
                'timeline': '1 week',
                'steps': ['Identify potential carpool partners', 'Set up schedule', 'Establish cost-sharing'],
                'icon': '👥'
            },
            {
                'id': 'eco_driving',
                'category': '🚗 Travel',
                'difficulty': 'Easy',
                'impact_level': 'Medium',
                'title': 'Practice Eco-Driving',
                'description': 'Adopt fuel-efficient driving habits and proper vehicle maintenance.',
                'potential_savings': 20,
                'cost': 'Low',
                'timeline': 'Immediate',
                'steps': ['Maintain proper tire pressure', 'Avoid rapid acceleration', 'Reduce idling time'],
                'icon': '🚗'
            }
        ])
    
    # Food recommendations
    if totals.get('food', 0) > 100:
        recs.extend([
            {
                'id': 'plant_based',
                'category': '🍎 Food',
                'difficulty': 'Medium',
                'impact_level': 'High',
                'title': 'Plant-Based Meals',
                'description': 'Replace 2 meat-based meals per week with plant-based alternatives.',
                'potential_savings': 35,
                'cost': 'Low',
                'timeline': '2 weeks',
                'steps': ['Research plant-based recipes', 'Plan meat-free days', 'Gradually increase frequency'],
                'icon': '🌱'
            },
            {
                'id': 'local_produce',
                'category': '🍎 Food',
                'difficulty': 'Easy',
                'impact_level': 'Medium',
                'title': 'Buy Local Produce',
                'description': 'Choose locally sourced fruits and vegetables to reduce transport emissions.',
                'potential_savings': 12,
                'cost': 'Medium',
                'timeline': 'Immediate',
                'steps': ['Find local farmers markets', 'Check product origins', 'Seasonal shopping'],
                'icon': '🏪'
            },
            {
                'id': 'reduce_waste',
                'category': '🍎 Food',
                'difficulty': 'Medium',
                'impact_level': 'Medium',
                'title': 'Reduce Food Waste',
                'description': 'Implement strategies to minimize food spoilage and waste.',
                'potential_savings': 18,
                'cost': 'None',
                'timeline': '1 week',
                'steps': ['Plan meals ahead', 'Proper food storage', 'Compost leftovers'],
                'icon': '🗑️'
            }
        ])
    
    # Goods recommendations
    if totals.get('goods', 0) > 50:
        recs.extend([
            {
                'id': 'secondhand',
                'category': '🛍️ Goods',
                'difficulty': 'Easy',
                'impact_level': 'Medium',
                'title': 'Buy Secondhand',
                'description': 'Choose pre-owned items for clothing, furniture, and electronics.',
                'potential_savings': 22,
                'cost': 'Low',
                'timeline': 'Immediate',
                'steps': ['Explore local thrift stores', 'Check online marketplaces', 'Quality assessment'],
                'icon': '🔄'
            },
            {
                'id': 'minimal_packaging',
                'category': '🛍️ Goods',
                'difficulty': 'Easy',
                'impact_level': 'Low',
                'title': 'Avoid Excessive Packaging',
                'description': 'Choose products with minimal or recyclable packaging.',
                'potential_savings': 10,
                'cost': 'None',
                'timeline': 'Immediate',
                'steps': ['Bring reusable bags', 'Choose bulk options', 'Avoid single-use plastics'],
                'icon': '📦'
            }
        ])
    
    return recs

def generate_conversational_response(user_input, totals, score, profile, conversation_history):
    """Generate AI response for chat conversation"""
    try:
        api_key = os.getenv('HUGGINGFACE_API_KEY')
        if not api_key:
            return random.choice([
                "I'd love to help with personalized advice, but I need API configuration. Meanwhile, try LED lighting and public transport for quick wins!",
                "For now, I can suggest general tips: reducing meat consumption and carpooling are great starting points for emission reduction.",
                "Simple changes like unplugging devices and buying local can significantly reduce your carbon footprint."
            ])
        
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Build context from user profile and emissions
        context = f"""
        User profile: {profile} with carbon score {score}/100.
        Monthly emissions - Energy: {totals.get('energy', 0)}kg, Travel: {totals.get('travel', 0)}kg, 
        Food: {totals.get('food', 0)}kg, Goods: {totals.get('goods', 0)}kg.
        
        Conversation history: {conversation_history[-3:] if conversation_history else 'First message'}
        User question: {user_input}
        
        Provide a helpful, concise response (under 100 words) about carbon reduction strategies.
        Focus on practical, actionable advice tailored to their emission profile.
        """
        
        payload = {
            "inputs": context,
            "parameters": {
                "max_length": 150,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            },
            "options": {"wait_for_model": True}
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '').strip()
                if generated_text:
                    return generated_text
        
        # Fallback responses
        return random.choice([
            "Based on your emissions, focus on public transport and energy-efficient appliances for the biggest impact.",
            "Consider plant-based meals and reducing car trips - these could significantly lower your carbon footprint.",
            "LED lighting, smart thermostats, and buying local are great starting points for your emission profile."
        ])
        
    except Exception as e:
        print(f"AI response error: {e}")
        return random.choice([
            "I suggest starting with easy wins like LED bulbs and reducing food waste.",
            "Public transportation and carpooling could greatly reduce your travel emissions.",
            "Try incorporating more plant-based meals and buying secondhand items when possible."
        ])

def calculate_progress(implemented_recommendations, all_recommendations):
    """Calculate progress metrics"""
    total_actions = len(all_recommendations)
    completed_actions = len(implemented_recommendations)
    
    total_potential_savings = sum(rec['potential_savings'] for rec in all_recommendations)
    achieved_savings = sum(rec['potential_savings'] for rec in all_recommendations 
                          if rec['id'] in implemented_recommendations)
    
    progress_percentage = (completed_actions / total_actions * 100) if total_actions > 0 else 0
    
    return {
        'total_actions': total_actions,
        'completed_actions': completed_actions,
        'progress_percentage': progress_percentage,
        'total_potential_savings': total_potential_savings,
        'achieved_savings': achieved_savings
    }

# ✅ STATE MANAGEMENT
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'implemented_recommendations' not in st.session_state:
    st.session_state.implemented_recommendations = set()
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = [
        {"role": "assistant", "content": "👋 Hello! I'm your CarbonLens AI assistant. I can help you understand your carbon footprint and suggest personalized reduction strategies. How can I assist you today?"}
    ]
if 'last_chat_input' not in st.session_state:
    st.session_state.last_chat_input = ""
if 'show_steps' not in st.session_state:
    st.session_state.show_steps = {}
if 'show_details' not in st.session_state:
    st.session_state.show_details = {}

# ✅ VALIDATE ENVIRONMENT
api_available = validate_environment()

# ✅ SAMPLE DATA (In a real app, this would come from user input or database)
totals = {"total": 580, "energy": 220, "travel": 180, "food": 120, "goods": 60}
score = 65
profile = "Urban Commuter"

# ✅ GENERATE RECOMMENDATIONS
recommendations = generate_dynamic_recommendations(totals, score, profile)

# ✅ METRICS SECTION
st.markdown("<h3 style='color:#f1f5f9;'>📊 Your Carbon Overview</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"<div class='metric'><h4>{score}/100</h4><p>Green Score</p></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric'><h4>{totals['total']} kg</h4><p>Monthly CO₂</p></div>", unsafe_allow_html=True)
with col3:
    highest = max([k for k in totals.keys() if k != 'total'], key=totals.get).title()
    st.markdown(f"<div class='metric'><h4>{highest}</h4><p>Highest Impact</p></div>", unsafe_allow_html=True)
with col4:
    progress_data = calculate_progress(st.session_state.implemented_recommendations, recommendations)
    st.markdown(f"<div class='metric'><h4>{progress_data['completed_actions']}/{progress_data['total_actions']}</h4><p>Actions Completed</p></div>", unsafe_allow_html=True)

st.markdown("---")

# ✅ PROGRESS TRACKING SECTION
if st.session_state.implemented_recommendations:
    st.markdown("<h3 style='color:#f1f5f9;'>🎯 Your Progress</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            "Actions Completed", 
            f"{progress_data['completed_actions']}/{progress_data['total_actions']}",
            f"{progress_data['progress_percentage']:.1f}%"
        )
        st.progress(progress_data['progress_percentage'] / 100)
    
    with col2:
        st.metric(
            "CO₂ Reduction Achieved", 
            f"{progress_data['achieved_savings']} kg/month",
            f"of {progress_data['total_potential_savings']} kg potential"
        )
        
        savings_percentage = (progress_data['achieved_savings'] / progress_data['total_potential_savings'] * 100) if progress_data['total_potential_savings'] > 0 else 0
        st.progress(savings_percentage / 100)

# ✅ RECOMMENDATIONS SECTION - FEATURE CARDS
st.markdown("<h3 style='color:#f1f5f9;'>📋 Personalized Recommendations</h3>", unsafe_allow_html=True)

if not recommendations:
    st.info("🎉 Great job! Your carbon footprint is already optimized. Keep up the good work!")
else:
    # Display recommendations in a grid of feature cards
    cols = st.columns(3)  # 3 columns for the grid
    
    for i, rec in enumerate(recommendations):
        col_idx = i % 3
        is_implemented = rec['id'] in st.session_state.implemented_recommendations
        
        with cols[col_idx]:
            # Feature Card
            st.markdown(f"""
            <div class="feature-card">
                <div>
                    <div style="font-size: 2.5rem; text-align: center; margin-bottom: 15px;">
                        {rec.get('icon', '🌱')}
                    </div>
                    <div class="category-badge">{rec['category']}</div>
                    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                        <span class="difficulty-badge">{rec['difficulty']}</span>
                        <span class="impact-badge">{rec['impact_level']} Impact</span>
                    </div>
                    <h4 style="color: #f1f5f9; margin-bottom: 12px; font-size: 1.1rem;">{rec['title']}</h4>
                    <p style="color: #94a3b8; margin-bottom: 15px; font-size: 0.9rem; line-height: 1.4;">{rec['description']}</p>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.05); padding: 12px; border-radius: 10px; margin-bottom: 15px;">
                        <div style="text-align: center;">
                            <div style="font-size: 0.8em; color: #cbd5e1;">Savings</div>
                            <div style="color: #00d4aa; font-weight: bold;">{rec['potential_savings']} kg</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 0.8em; color: #cbd5e1;">Cost</div>
                            <div style="color: #6c63ff; font-weight: bold;">{rec.get('cost', 'Varies')}</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 0.8em; color: #cbd5e1;">Time</div>
                            <div style="color: #ff6b6b; font-weight: bold;">{rec.get('timeline', 'Varies')}</div>
                        </div>
                    </div>
                </div>
                
                <div>
                    <!-- Action Buttons -->
                    <div class="action-buttons">
                        <button class="emoji-button" onclick="showSteps('{rec['id']}')" title="Implementation Steps">📋</button>
                        <button class="emoji-button" onclick="showDetails('{rec['id']}')" title="Learn More">💡</button>
                    </div>
                    
                    <!-- Implementation Checkbox -->
                    <div class="implemented-checkbox">
                        <label style="color: #cbd5e1; font-size: 0.9em;">
                            <input type="checkbox" id="impl_{rec['id']}" {'checked' if is_implemented else ''} 
                                   onchange="toggleImplementation('{rec['id']}')">
                            Mark as implemented
                        </label>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Handle button clicks for this card
            if st.session_state.show_steps.get(rec['id']):
                with st.expander(f"📋 Implementation Steps for {rec['title']}", expanded=True):
                    for step in rec.get('steps', []):
                        st.write(f"• {step}")
                st.session_state.show_steps[rec['id']] = False
            
            if st.session_state.show_details.get(rec['id']):
                with st.expander(f"💡 More about {rec['title']}", expanded=True):
                    st.write(f"""
                    **Impact Details:**
                    - **Category**: {rec['category']}
                    - **Difficulty**: {rec['difficulty']}
                    - **Impact Level**: {rec['impact_level']}
                    - **Potential Savings**: {rec['potential_savings']} kg CO₂/month
                    - **Cost**: {rec.get('cost', 'Varies')}
                    - **Timeline**: {rec.get('timeline', 'Varies')}
                    """)
                st.session_state.show_details[rec['id']] = False

# ✅ CHAT SECTION
st.markdown("---")
st.markdown("<h3 style='color:#f1f5f9;'>💬 CarbonLens AI Assistant</h3>", unsafe_allow_html=True)

# Chat input at the bottom of the page
with st.container():
    user_input = st.text_input(
        "Ask me about carbon reduction strategies:",
        placeholder="e.g., How can I reduce my travel emissions?",
        key="chat_input"
    )
    
    if user_input and user_input != st.session_state.last_chat_input:
        # Add user message to conversation
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        st.session_state.conversation.append(user_input)
        
        # Generate AI response
        with st.spinner("🤖 Thinking..."):
            ai_response = generate_conversational_response(
                user_input, 
                totals, 
                score, 
                profile, 
                st.session_state.conversation
            )
        
        # Add AI response to conversation
        st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})
        st.session_state.conversation.append(ai_response)
        
        # Update last processed message
        st.session_state.last_chat_input = user_input
        
        # Rerun to update the chat display
        st.rerun()

# Display conversation
if st.session_state.chat_messages:
    st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style='text-align: right; margin: 10px 0;'>
                <div style='background: linear-gradient(135deg, #00d4aa, #6c63ff); color: white; padding: 12px 16px; border-radius: 18px 18px 0 18px; display: inline-block; max-width: 80%;'>
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: left; margin: 10px 0;'>
                <div style='background: rgba(108, 99, 255, 0.2); border: 1px solid rgba(108, 99, 255, 0.3); color: #f1f5f9; padding: 12px 16px; border-radius: 18px 18px 18px 0; display: inline-block; max-width: 80%;'>
                    {msg["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ✅ JAVASCRIPT FOR INTERACTIONS
st.markdown("""
<script>
function showSteps(recommendationId) {
    // This will trigger a Streamlit rerun with the show_steps state updated
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: {action: 'show_steps', id: recommendationId}
    }, '*');
}

function showDetails(recommendationId) {
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: {action: 'show_details', id: recommendationId}
    }, '*');
}

function toggleImplementation(recommendationId) {
    const checkbox = document.getElementById('impl_' + recommendationId);
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: {action: 'toggle_impl', id: recommendationId, checked: checkbox.checked}
    }, '*');
}
</script>

<!-- Floating Chat Button -->
<div id="chatButton" onclick="scrollToChat()">
    <span>🤖</span>
</div>

<script>
function scrollToChat() {
    // Scroll to the chat section
    const chatSection = window.parent.document.querySelector('h3:contains("💬 CarbonLens AI Assistant")');
    if (chatSection) {
        chatSection.scrollIntoView({ behavior: 'smooth' });
    }
}
</script>
""", unsafe_allow_html=True)

# ✅ FOOTER
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #64748b; padding: 2rem;'>"
    "💚 Made with CarbonLens - Tracking your journey to sustainability"
    "</div>",
    unsafe_allow_html=True
)