import os
import requests
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import streamlit as st
from app.components.forms import lifestyle_form
from app.components.charts import donut_breakdown, trend_line, gauge
from app.components.scorecard import score_card
from app.components.toasts import toast_success, toast_warn
from app.components.charts import kpi_tiles
from app.utils_local_calc import local_compute  # fallback calc

st.set_page_config(page_title="Analyze Footprint", page_icon="📈", layout="wide")

# ✅ COLOR PALETTE - BLUE/PURPLE THEME
st.markdown("""
<style>
:root {
    --primary: #6366f1;
    --primary-light: #8b5cf6;
    --secondary: #06b6d4;
    --accent: #f59e0b;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
}

.page-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 10px;
    padding: 20px;
}

.subtitle {
    text-align: center;
    color: #c8d5ca;
    margin-bottom: 40px;
    font-size: 18px;
}

.card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 24px;
    margin: 10px 0;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    border-color: var(--primary);
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.2);
}

.tip {
    background: rgba(99, 102, 241, 0.15);
    border-left: 4px solid var(--primary);
}

.tip .label {
    background: var(--primary);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
    margin-bottom: 8px;
}

.tip-text {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
    margin: 8px 0;
}

.muted {
    color: #c8d5ca;
    font-size: 14px;
}

.stButton button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin: 2px;
}

.badge-primary { background: rgba(99, 102, 241, 0.2); color: var(--primary); }
.badge-secondary { background: rgba(6, 182, 212, 0.2); color: var(--secondary); }
.badge-accent { background: rgba(245, 158, 11, 0.2); color: var(--accent); }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🌍 Carbon Footprint Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Understand your environmental impact and discover personalized ways to reduce it</div>', unsafe_allow_html=True)

API = "http://localhost:8000/api"

# ✅ PERSONALIZED QUESTIONNAIRE FUNCTION - COMPREHENSIVE FIELDS
def personalized_questionnaire():
    """Comprehensive personalized questionnaire for custom profile"""
    st.markdown("### 🎯 Tell Us About Your Lifestyle")
    
    if 'questionnaire_step' not in st.session_state:
        st.session_state.questionnaire_step = 0
    if 'custom_profile_data' not in st.session_state:
        st.session_state.custom_profile_data = {}
    
    steps = [
        "🏠 Housing & Energy",
        "🚗 Transportation", 
        "🍽️ Diet & Food",
        "🛒 Shopping Habits",
        "🌱 Sustainability Practices"
    ]
    
    progress = st.session_state.questionnaire_step / (len(steps) - 1) if len(steps) > 1 else 0
    st.progress(progress)
    st.caption(f"Step {st.session_state.questionnaire_step + 1} of {len(steps)}: {steps[st.session_state.questionnaire_step]}")
    
    # Step 1: Housing & Energy
    if st.session_state.questionnaire_step == 0:
        st.markdown("#### 🏠 Your Living Situation")
        
        col1, col2 = st.columns(2)
        with col1:
            housing_type = st.selectbox(
                "Type of Residence",
                ["Apartment/Condo", "Single Family Home", "Townhouse", "Student Housing", "Other"]
            )
            home_size = st.select_slider(
                "Home Size",
                options=["Small (< 100m²)", "Medium (100-200m²)", "Large (> 200m²)"]
            )
        
        with col2:
            residents = st.number_input("Number of People in Household", min_value=1, max_value=10, value=2)
            heating_type = st.selectbox(
                "Primary Heating Source",
                ["Natural Gas", "Electric", "Oil", "Heat Pump", "Other"]
            )
        
        electricityKwh = st.slider("Monthly Electricity Usage (kWh)", 0, 2000, 300)
        naturalGasTherms = st.slider("Monthly Natural Gas (therms)", 0, 200, 50)
        
        st.session_state.custom_profile_data.update({
            'housing_type': housing_type,
            'home_size': home_size,
            'residents': residents,
            'heating_type': heating_type,
            'electricityKwh': electricityKwh,
            'naturalGasTherms': naturalGasTherms
        })
    
    # Step 2: Transportation
    elif st.session_state.questionnaire_step == 1:
        st.markdown("#### 🚗 Your Daily Commute")
        
        commute_method = st.selectbox(
            "Primary Commute Method",
            ["Car (driver)", "Car (passenger)", "Public Transit", "Bicycle", "Walk", "Motorcycle", "Telecommute"]
        )
        
        carKm = st.slider("Monthly Car Distance (km)", 0, 2000, 300)
        busKm = st.slider("Monthly Bus Distance (km)", 0, 1000, 50)
        commute_days = st.slider("Commute Days per Week", 0, 7, 5)
        
        st.markdown("#### ✈️ Travel Habits")
        flights_per_year = st.slider("Number of Flights per Year", 0, 50, 2)
        car_type = st.selectbox(
            "If you drive, what type of vehicle?",
            ["Don't own a car", "Gasoline", "Diesel", "Hybrid", "Electric", "Plug-in Hybrid"]
        )
        
        st.session_state.custom_profile_data.update({
            'commute_method': commute_method,
            'carKm': carKm,
            'busKm': busKm,
            'commute_days': commute_days,
            'flights_per_year': flights_per_year,
            'car_type': car_type
        })
    
    # Step 3: Diet & Food
    elif st.session_state.questionnaire_step == 2:
        st.markdown("#### 🍽️ Your Eating Habits")
        
        diet_type = st.selectbox(
            "Primary Diet",
            ["Omnivore (balanced)", "Omnivore (meat-heavy)", "Pescatarian", "Vegetarian", "Vegan", "Flexitarian"]
        )
        
        food_organic = st.slider("Percentage of Organic Food", 0, 100, 20)
        food_waste = st.select_slider(
            "Food Waste Level",
            options=["Minimal", "Low", "Moderate", "High"]
        )
        
        # Convert diet type to food emissions
        diet_factors = {
            "Vegan": 1.5, "Vegetarian": 2.0, "Pescatarian": 2.5,
            "Flexitarian": 3.0, "Omnivore (balanced)": 3.5, "Omnivore (meat-heavy)": 4.5
        }
        foodEmissions = diet_factors.get(diet_type, 3.5)
        
        st.session_state.custom_profile_data.update({
            'diet_type': diet_type,
            'food_organic': food_organic,
            'food_waste': food_waste,
            'foodEmissions': foodEmissions
        })
    
    # Step 4: Shopping Habits
    elif st.session_state.questionnaire_step == 3:
        st.markdown("#### 🛒 Your Consumption Patterns")
        
        shopping_frequency = st.select_slider(
            "General Shopping Frequency",
            options=["Minimalist", "Infrequent", "Moderate", "Frequent", "Very Frequent"]
        )
        
        shopping_online = st.slider("Percentage of Online Shopping", 0, 100, 30)
        goodsEmissions = st.slider("Monthly Goods Emissions (kg CO₂)", 0, 500, 200)
        
        st.session_state.custom_profile_data.update({
            'shopping_frequency': shopping_frequency,
            'shopping_online': shopping_online,
            'goodsEmissions': goodsEmissions
        })
    
    # Step 5: Sustainability Practices
    elif st.session_state.questionnaire_step == 4:
        st.markdown("#### 🌱 Your Current Sustainability Efforts")
        
        current_practices = st.multiselect(
            "Which sustainability practices do you currently follow?",
            [
                "Recycling regularly", "Composting", "Using reusable bags",
                "Reducing plastic use", "Conserving water", "Using public transit",
                "Energy conservation", "Plant-based diet", "Supporting eco-friendly brands",
                "Carbon offset purchases", "None currently"
            ]
        )
        
        willingness_change = st.select_slider(
            "How willing are you to make lifestyle changes?",
            options=["Not willing", "Slightly willing", "Moderately willing", "Very willing", "Extremely willing"]
        )
        
        st.session_state.custom_profile_data.update({
            'current_practices': current_practices,
            'willingness_change': willingness_change
        })
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.session_state.questionnaire_step > 0:
            if st.button("⬅️ Previous"):
                st.session_state.questionnaire_step -= 1
                st.rerun()
    
    with col3:
        if st.session_state.questionnaire_step < len(steps) - 1:
            if st.button("Next ➡️", type="primary"):
                st.session_state.questionnaire_step += 1
                st.rerun()
        else:
            if st.button("🎯 Complete Profile", type="primary"):
                processed_data = process_custom_profile(st.session_state.custom_profile_data)
                st.session_state.custom_profile_processed = processed_data
                st.session_state.show_questionnaire = False
                st.session_state.selected_profile = "Custom"
                st.rerun()

def process_custom_profile(data):
    """Convert questionnaire responses to calculation inputs"""
    processed = {}
    
    # Core calculation fields (required by local_compute)
    processed['electricityKwh'] = data.get('electricityKwh', 300)
    processed['naturalGasTherms'] = data.get('naturalGasTherms', 50)
    processed['carKm'] = data.get('carKm', 0)
    processed['busKm'] = data.get('busKm', 0)
    processed['foodEmissions'] = data.get('foodEmissions', 3.5)
    processed['goodsEmissions'] = data.get('goodsEmissions', 200)
    
    # Additional fields for comprehensive analysis
    processed['housing_type'] = data.get('housing_type')
    processed['residents'] = data.get('residents', 2)
    processed['flights_per_year'] = data.get('flights_per_year', 0)
    processed['food_organic'] = data.get('food_organic', 20)
    processed['shopping_frequency'] = data.get('shopping_frequency', 'Moderate')
    
    return processed

# ✅ PROFILE SELECTOR - COMPREHENSIVE FIELDS
st.markdown("### 🚀 Quick Start - Choose Your Profile")
profile_cols = st.columns(4)

# Demo profiles with comprehensive fields
demo_profiles = {
    "Urban Commuter": {
        "electricityKwh": 350, "naturalGasTherms": 60, "carKm": 600, "busKm": 100, 
        "foodEmissions": 3.5, "goodsEmissions": 250, "housing_type": "Apartment/Condo",
        "residents": 2, "flights_per_year": 4
    },
    "Student Hostel": {
        "electricityKwh": 150, "naturalGasTherms": 20, "carKm": 50, "busKm": 200, 
        "foodEmissions": 2.0, "goodsEmissions": 150, "housing_type": "Student Housing",
        "residents": 4, "flights_per_year": 2
    },
    "Frequent Flyer": {
        "electricityKwh": 400, "naturalGasTherms": 80, "carKm": 1200, "busKm": 50, 
        "foodEmissions": 4.5, "goodsEmissions": 300, "housing_type": "Single Family Home",
        "residents": 3, "flights_per_year": 12
    }
}

with profile_cols[0]:
    if st.button("🏙️ Urban Commuter", use_container_width=True, key="urban"):
        st.session_state.selected_profile = "Urban Commuter"
        st.session_state.demo_data = demo_profiles["Urban Commuter"]

with profile_cols[1]:
    if st.button("🎓 Student Life", use_container_width=True, key="student"):
        st.session_state.selected_profile = "Student Hostel"
        st.session_state.demo_data = demo_profiles["Student Hostel"]

with profile_cols[2]:
    if st.button("✈️ Frequent Flyer", use_container_width=True, key="flyer"):
        st.session_state.selected_profile = "Frequent Flyer"
        st.session_state.demo_data = demo_profiles["Frequent Flyer"]

with profile_cols[3]:
    if st.button("🎯 Custom Profile", use_container_width=True, key="custom", type="secondary"):
        st.session_state.show_questionnaire = True

# Show questionnaire if triggered
if st.session_state.get('show_questionnaire', False):
    st.markdown("---")
    personalized_questionnaire()
else:
    st.markdown("---")

    # ✅ MAIN LAYOUT WITH TABS
    tab1, tab2, tab3 = st.tabs(["📝 Lifestyle Assessment", "📊 Results Dashboard", "🤖 AI Recommendations"])

    with tab1:
        # Use custom profile data if available, else use demo data
        if st.session_state.get('selected_profile') == "Custom" and st.session_state.get('custom_profile_processed'):
            form_values = st.session_state.custom_profile_processed
            st.success("✅ Using your custom profile data!")
        elif st.session_state.get('demo_data'):
            form_values = st.session_state.demo_data
            st.info(f"🏷️ Using {st.session_state.selected_profile} profile")
        else:
            # Use the lifestyle form component
            form_values = lifestyle_form(st.session_state.get('selected_profile', "— Select —"))
        
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.markdown("### Your Lifestyle Details")
            if st.session_state.get('selected_profile') == "Custom":
                # Show summary of custom data
                with st.expander("📋 Your Custom Profile Summary"):
                    st.json(st.session_state.get('custom_profile_data', {}))
            elif not st.session_state.get('demo_data'):
                # Show the standard form for manual input
                st.info("ℹ️ Fill out the form or select a demo profile above")
            else:
                # Show the current demo data being used
                st.write("**Current Profile Data:**")
                st.json({k: v for k, v in form_values.items() if k in ['electricityKwh', 'naturalGasTherms', 'carKm', 'busKm', 'foodEmissions', 'goodsEmissions']})
        
        with col2:
            st.markdown("### 🎯 Action Center")
            run = st.button("🚀 Compute My Carbon Footprint", use_container_width=True, type="primary")
            
            st.markdown("---")
            st.markdown("""
            <div class='card'>
                <h4>🔍 How It Works</h4>
                <p style='color: #c8d5ca; font-size: 14px;'>
                • Electricity: 0.82 kg CO₂ per kWh<br>
                • Natural Gas: 5.3 kg CO₂ per therm<br>
                • Car Travel: 0.21 kg CO₂ per km<br>
                • Bus Travel: 0.09 kg CO₂ per km<br>
                • Food: Based on diet type (1.5-4.5 kg CO₂/day)<br>
                • Goods: Direct emissions input<br>
                • Green Score: 0-100 scale
                </p>
            </div>
            """, unsafe_allow_html=True)

    # ✅ RESULTS DASHBOARD TAB
    with tab2:
        if "last_result" in st.session_state:
            result = st.session_state["last_result"]
            totals = result["totals"]
            score = result["score"]
            trend = result.get("trend", [])
            
            # KPI Tiles Section
            st.markdown("### 📊 Your Carbon Footprint Dashboard")
            kpi_tiles(
                total_kg=totals["total"],
                energy_kg=totals["energy"],
                travel_kg=totals["travel"],
                food_kg=totals["food"]
            )
            
            # Charts Section
            st.markdown("### 📈 Detailed Analysis")
            c1, c2, c3 = st.columns([1.2, 1.2, 1])
            
            with c1:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                donut_breakdown(
                    {
                        "Energy": totals["energy"],
                        "Travel": totals["travel"],
                        "Food": totals["food"],
                        "Goods": totals.get("goods", 0)
                    },
                    title="🌿 Emission Breakdown"
                )
                st.markdown("</div>", unsafe_allow_html=True)
            
            with c2:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                trend_line(trend)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with c3:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                gauge(score)
                score_card(score)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Leaderboard Info
            st.markdown("### 🏆 Leaderboard Entry")
            st.info(f"Your Green Score of **{score}** has been saved to the leaderboard!")

    # ✅ AI RECOMMENDATIONS TAB
    with tab3:
        if "last_result" in st.session_state:
            st.markdown("### 🤖 Personalized Recommendations")
            
            tips = [
                {"area": "🚗 Travel", "text": "Reduce car travel by using public transport more often", "impact_kg_month": 45, "confidence": 0.85},
                {"area": "⚡ Energy", "text": "Switch to energy-efficient appliances and LED lighting", "impact_kg_month": 25, "confidence": 0.90},
                {"area": "🍽️ Food", "text": "Consider incorporating more plant-based meals", "impact_kg_month": 30, "confidence": 0.80},
                {"area": "🛒 Shopping", "text": "Choose products with minimal packaging and buy local", "impact_kg_month": 20, "confidence": 0.75},
            ]
            
            for i, t in enumerate(tips):
                st.markdown(f"""
                <div class="card tip">
                    <div class="label">{t['area']}</div>
                    <div class="tip-text">{t['text']}</div>
                    <div class="muted">🌱 Saves <b>{t['impact_kg_month']} kg CO₂/month</b> • 🎯 {int(t['confidence']*100)}% confidence</div>
                </div>
                """, unsafe_allow_html=True)

    # ✅ EMPTY STATE - MOVED INSIDE THE ELSE BLOCK
    if "last_result" not in st.session_state:
        with tab1:
            st.markdown("""
            <div style='text-align: center; padding: 60px 20px; color: #c8d5ca;'>
                <div style='font-size: 64px; margin-bottom: 20px;'>🌍</div>
                <h3>Ready to Discover Your Environmental Impact?</h3>
                <p>Choose a profile or create a custom one, then click "Compute My Carbon Footprint" to begin!</p>
                <div style='margin-top: 30px;'>
                    <span class='badge badge-primary'>Comprehensive Analysis</span>
                    <span class='badge badge-secondary'>Green Scoring</span>
                    <span class='badge badge-accent'>12-Month Forecast</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ✅ FOOTPRINT COMPUTATION - MATCHING BACKEND SCHEMA
if 'run' in locals() and run:
    with st.spinner('🔄 Analyzing your carbon footprint...'):
        try:
            # Prepare payload matching backend LifestyleInput schema
            payload = {
                "electricityKwh": form_values.get('electricityKwh', 0),
                "naturalGasTherms": form_values.get('naturalGasTherms', 0),
                "carKm": form_values.get('carKm', 0),
                "busKm": form_values.get('busKm', 0),
                "diet": "mixed",  # Required by schema, but we'll use foodEmissions for calculation
                "foodEmissions": form_values.get('foodEmissions', 3.5),
                "goodsEmissions": form_values.get('goodsEmissions', 0)
            }
            
            # Call your backend API
            r = requests.post(f"{API}/footprint/compute", json=payload, timeout=10)
            if r.status_code == 200:
                result = r.json()
                toast_success("✅ Footprint analysis complete! Check your dashboard.")
            else:
                raise Exception(f"API Error: {r.status_code} - {r.text}")
                
        except Exception as e:
            toast_warn(f"⚠️ Using local calculator - {str(e)}")
            # Fall back to local calculator
            local_form_values = {
                'electricityKwh': form_values.get('electricityKwh', 0),
                'naturalGasTherms': form_values.get('naturalGasTherms', 0),
                'carKm': form_values.get('carKm', 0),
                'busKm': form_values.get('busKm', 0),
                'foodEmissions': form_values.get('foodEmissions', 3.5),
                'goodsEmissions': form_values.get('goodsEmissions', 0)
            }
            result = local_compute(local_form_values)

    # Store result in session state
    st.session_state["last_result"] = result
    st.rerun()
