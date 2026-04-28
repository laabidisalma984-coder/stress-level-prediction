import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from stress_prediction_interface import predict_stress_level
import warnings
import json
import os
from datetime import datetime
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Stress Predictor Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
        .main { padding-top: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        h1 { color: #1f77b4; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.1); font-size: 2.5rem; }
        h2 { color: #1f77b4; border-bottom: 3px solid #1f77b4; padding-bottom: 0.5rem; }
        .prediction-low { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); padding: 1.5rem; border-radius: 0.75rem; border-left: 5px solid #28a745; }
        .prediction-moderate { background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); padding: 1.5rem; border-radius: 0.75rem; border-left: 5px solid #ffc107; }
        .prediction-high { background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); padding: 1.5rem; border-radius: 0.75rem; border-left: 5px solid #dc3545; }
        .tips-box { background: linear-gradient(135deg, #e0f7ff 0%, #fff0e6 100%); padding: 1.5rem; border-radius: 0.75rem; border-left: 4px solid #00bcd4; }
        .success-badge { background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%); padding: 1rem; border-radius: 0.75rem; text-align: center; margin: 0.5rem 0; font-weight: bold; }
        .stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: bold; border-radius: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

def load_history():
    if os.path.exists('prediction_history.json'):
        try:
            with open('prediction_history.json', 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open('prediction_history.json', 'w') as f:
        json.dump(history, f, indent=2)

st.session_state.prediction_history = load_history()

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================
st.sidebar.markdown("# 🎓 Stress Predictor Pro")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📍 Navigate:",
    ["🔮 Predict My Stress", "📊 Analytics Hub", "📈 My Progress", "💡 Tips", "🏆 Achievements", "📱 Quick Check"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Quick Stats")
if st.session_state.prediction_history:
    avg_stress = sum([p['stress_level'] for p in st.session_state.prediction_history]) / len(st.session_state.prediction_history)
    st.sidebar.metric("Average Stress", f"{avg_stress:.2f}/10")
    st.sidebar.metric("Total Predictions", len(st.session_state.prediction_history))
    st.sidebar.metric("Latest", f"{st.session_state.prediction_history[-1]['stress_level']:.2f}/10")
else:
    st.sidebar.info("👋 No predictions yet. Start now!")

# ============================================================================
# PAGE 1: PREDICT MY STRESS
# ============================================================================
if page == "🔮 Predict My Stress":
    st.markdown("# 🔮 Your Stress Prediction")
    st.markdown("**Get personalized insights about your stress level**")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Personal Information")
        age = st.number_input("Age", min_value=18, max_value=50, value=21)
        degree = st.selectbox("Degree Type", ["licence", "cycle d'ingénieur", "mastère", "préparatoire intégrée", "doctorat", "médecine", "pharmacie", "Bachelor degree at TBS"])
        year = st.selectbox("Year of Study", ["1st", "2nd", "3rd", "4th", "5th"])
        major = st.text_input("Major/Field", placeholder="e.g., Psychology, IT, Medicine")
    
    with col2:
        st.markdown("### 😴 Lifestyle Factors")
        sleep = st.select_slider("Sleep Per Night", options=["Less than 5 hours", "5–6 hours", "7–8 hours", "More than 8 hours"], value="7–8 hours")
        screen = st.select_slider("Screen Time (excluding study)", options=["Less than 2 hours", "2–4 hours", "4–6 hours", "More than 6 hours"], value="4–6 hours")
        exercise = st.radio("Physical Activity", ["Yes", "No"], horizontal=True)
        exercise = "yes" if exercise == "Yes" else "no"
        caffeine = st.slider("Caffeine Drinks/Day", 0, 3, 1)
    
    st.divider()
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 📚 Academic")
        study = st.select_slider("Study Hours/Week", options=["Less than 10 hours", "10–20 hours", "20–30 hours", "More than 30 hours"], value="10–20 hours")
        exam = st.radio("Exams in 2 weeks?", ["No", "Yes"], horizontal=True)
        exam = "yes" if exam == "Yes" else "no"
    
    with col4:
        st.markdown("### ⚖️ Workload")
        workload = st.select_slider("Academic Workload", options=["low", "moderate", "high"], value="moderate")
    
    st.divider()
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        predict_button = st.button("🔮 PREDICT MY STRESS", use_container_width=True, type="primary")
    
    if predict_button:
        if not major:
            st.error("❌ Please enter your major")
        else:
            result = predict_stress_level(age, degree, year, major, sleep, screen, exercise, str(caffeine), study, exam, workload.lower())
            
            if 'error' in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                stress_level = result['predicted_stress_level']
                
                # Save to history
                prediction_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "stress_level": stress_level,
                    "category": result['stress_category'],
                    "age": age, "degree": degree, "major": major,
                    "sleep": sleep, "exercise": exercise, "workload": workload
                }
                st.session_state.prediction_history.append(prediction_entry)
                save_history(st.session_state.prediction_history)
                
                # Display result
                if stress_level < 4:
                    st.markdown(f'<div class="prediction-low"><h3>✅ Low Stress: {stress_level:.2f}/10</h3><p>Excellent! Keep up these habits!</p></div>', unsafe_allow_html=True)
                    color = "green"
                elif stress_level < 7:
                    st.markdown(f'<div class="prediction-moderate"><h3>⚠️ Moderate Stress: {stress_level:.2f}/10</h3><p>Consider some adjustments.</p></div>', unsafe_allow_html=True)
                    color = "orange"
                else:
                    st.markdown(f'<div class="prediction-high"><h3>🚨 High Stress: {stress_level:.2f}/10</h3><p>Seek support immediately.</p></div>', unsafe_allow_html=True)
                    color = "red"
                
                # Gauge
                st.markdown("### 📊 Visualization")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta", value=stress_level,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Stress Level (1-10)", 'font': {'size': 20}},
                    delta={'reference': 5.89, 'prefix': "vs Avg: "},
                    gauge={
                        'axis': {'range': [0, 10]},
                        'bar': {'color': color, 'thickness': 0.7},
                        'steps': [
                            {'range': [0, 3], 'color': "#90EE90"},
                            {'range': [3, 7], 'color': "#FFE4B5"},
                            {'range': [7, 10], 'color': "#FFB6C6"}
                        ]
                    },
                    number={'suffix': "/10", 'font': {'size': 35}}
                ))
                fig.update_layout(height=400, margin=dict(l=0, r=0, t=50, b=0))
                st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations
                st.markdown("### 💡 Your Plan")
                col_rec1, col_rec2 = st.columns(2)
                with col_rec1:
                    st.markdown("**🎯 This Week:**")
                    if workload == "high": st.write("• Break tasks into chunks")
                    if exercise == "no": st.write("• Add 20-30 min exercise")
                    if sleep == "Less than 5 hours": st.write("• Prioritize sleep")
                    if stress_level > 7: st.write("• Build support network")
                
                with col_rec2:
                    st.markdown("**📋 Long-term:**")
                    st.write("• Practice time management")
                    st.write("• Maintain consistent sleep")
                    st.write("• Exercise 3-4x/week")
                    st.write("• Limit caffeine after 2 PM")
                
                st.success("✅ Prediction saved!")

# ============================================================================
# PAGE 2: ANALYTICS HUB
# ============================================================================
elif page == "📊 Analytics Hub":
    st.markdown("# 📊 Analytics Hub")
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Average Stress", "5.89/10", "All Students")
    col2.metric("Your Average", f"{sum([p['stress_level'] for p in st.session_state.prediction_history]) / max(1, len(st.session_state.prediction_history)):.2f}/10", f"{len(st.session_state.prediction_history)} predictions")
    col3.metric("Model Accuracy", "51.09%", "R² Score")
    col4.metric("Prediction Error", "±1.42", "Average")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ⭐ Top Stress Factors")
        factors = ["Workload", "Major", "Sleep", "Exams", "Age"]
        importance = [35.9, 11.5, 11.4, 9.0, 7.9]
        fig = go.Figure(data=[go.Bar(y=factors, x=importance, orientation='h',
            marker=dict(color=importance, colorscale='Reds', showscale=False),
            text=[f"{imp:.1f}%" for imp in importance], textposition='outside')])
        fig.update_layout(title="Feature Importance", xaxis_title="%", height=400, showlegend=False, margin=dict(l=100))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Stress Distribution")
        stress_levels = list(range(1, 11))
        counts = [15, 20, 35, 42, 55, 68, 75, 82, 45, 22]
        fig = px.bar(x=stress_levels, y=counts, title="Distribution (545 Students)", color=counts, color_continuous_scale='RdYlGn_r')
        fig.update_layout(height=400, xaxis_title="Stress Level", yaxis_title="Students")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE 3: MY PROGRESS
# ============================================================================
elif page == "📈 My Progress":
    st.markdown("# 📈 Your Progress")
    st.divider()
    
    if not st.session_state.prediction_history:
        st.info("📝 No data yet. Make your first prediction!")
    else:
        df = pd.DataFrame(st.session_state.prediction_history)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Stress", f"{df['stress_level'].mean():.2f}/10")
        col2.metric("Best", f"{df['stress_level'].min():.2f}/10", "Lowest")
        col3.metric("Peak", f"{df['stress_level'].max():.2f}/10", "Highest")
        
        st.divider()
        
        st.markdown("### 📈 Trend")
        fig = px.line(df, y='stress_level', markers=True, title="Stress Over Time",
                     color_discrete_sequence=['#1f77b4'])
        fig.add_hline(y=5.89, line_dash="dash", line_color="red", annotation_text="Average")
        fig.update_layout(height=400, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        st.markdown("### 📥 Export Data")
        csv = df.to_csv(index=False)
        st.download_button("📊 Download as CSV", data=csv, file_name="stress_history.csv")

# ============================================================================
# PAGE 4: TIPS
# ============================================================================
elif page == "💡 Tips":
    st.markdown("# 💡 Stress Management Tips")
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 😴 Sleep (11.4%)")
        st.markdown('''<div class="tips-box">
        <b>Why:</b> 2nd biggest factor<br>
        <b>Target:</b> 7-8 hours<br>
        <b>Tips:</b><br>
        ✅ Consistent bedtime<br>
        ✅ No screens 30 min before<br>
        ✅ Cool, dark room<br>
        ✅ Limit caffeine after 2 PM
        </div>''', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🎓 Workload (35.9%)")
        st.markdown('''<div class="tips-box">
        <b>Why:</b> #1 stress factor<br>
        <b>Action:</b> Plan ahead<br>
        <b>Tips:</b><br>
        ✅ Use planner/calendar<br>
        ✅ Break into chunks<br>
        ✅ Prioritize top 3 tasks<br>
        ✅ Talk to professors
        </div>''', unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 🏃 Exercise")
        st.markdown('''<div class="tips-box">
        <b>Benefits:</b><br>
        ✅ Reduces tension<br>
        ✅ Boosts mood<br>
        ✅ Improves sleep<br>
        ✅ Builds resilience<br>
        <b>Aim:</b> 30 min daily
        </div>''', unsafe_allow_html=True)
    
    with col4:
        st.markdown("### ☕ Caffeine & Screens")
        st.markdown('''<div class="tips-box">
        <b>Caffeine:</b><br>
        • 1-2 drinks optimal<br>
        • Avoid after 2 PM<br>
        <b>Screens:</b><br>
        • 4-6 hrs outside class<br>
        • No screens before bed<br>
        • 20-20-20 breaks
        </div>''', unsafe_allow_html=True)

# ============================================================================
# PAGE 5: ACHIEVEMENTS
# ============================================================================
elif page == "🏆 Achievements":
    st.markdown("# 🏆 Your Achievements")
    st.divider()
    
    achievements = []
    
    if len(st.session_state.prediction_history) >= 1:
        achievements.append(("🌟 First Step", "Made first prediction"))
    if len(st.session_state.prediction_history) >= 5:
        achievements.append(("📊 Data Collector", "5 predictions"))
    if len(st.session_state.prediction_history) >= 10:
        achievements.append(("📈 Tracker Pro", "10 predictions"))
    
    if st.session_state.prediction_history:
        avg = sum([p['stress_level'] for p in st.session_state.prediction_history]) / len(st.session_state.prediction_history)
        if avg < 4:
            achievements.append(("✨ Zen Master", "Avg stress < 4"))
        if avg < 5:
            achievements.append(("😊 Happy", "Avg stress < 5"))
    
    if achievements:
        cols = st.columns(2)
        for idx, (badge, desc) in enumerate(achievements):
            with cols[idx % 2]:
                st.markdown(f'<div class="success-badge">{badge}<br><small>{desc}</small></div>', unsafe_allow_html=True)
    else:
        st.info("🎯 Make predictions to unlock achievements!")

# ============================================================================
# PAGE 6: QUICK CHECK
# ============================================================================
elif page == "📱 Quick Check":
    st.markdown("# 📱 30-Second Check-In")
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sleep_q = st.radio("Sleep?", ["Great (7-8h)", "OK (5-7h)", "Bad (<5h)"])
    
    with col2:
        work_q = st.radio("Workload?", ["Light", "Moderate", "Heavy"])
    
    with col3:
        energy_q = st.radio("Energy?", ["High", "Medium", "Low"])
    
    st.divider()
    
    if st.button("📊 Get Insight", use_container_width=True, type="primary"):
        score = 5
        score += 2 if sleep_q == "Bad (<5h)" else (0.5 if sleep_q == "OK (5-7h)" else 0)
        score += 2 if work_q == "Heavy" else (1 if work_q == "Moderate" else 0)
        score += 1.5 if energy_q == "Low" else (0.5 if energy_q == "Medium" else 0)
        score = min(10, max(1, score))
        
        if score < 4:
            st.markdown(f'<div class="prediction-low"><h3>✅ Great! {score:.1f}/10</h3></div>', unsafe_allow_html=True)
        elif score < 7:
            st.markdown(f'<div class="prediction-moderate"><h3>⚠️ Moderate {score:.1f}/10</h3></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="prediction-high"><h3>🚨 High {score:.1f}/10</h3></div>', unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("**Stress Predictor Pro v2.0** | 🎓 For University Students | Built with ❤️")
