import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from stress_prediction_interface import predict_stress_level
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Stress Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1f77b4;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        h2 {
            color: #1f77b4;
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 0.5rem;
        }
        .prediction-low {
            background-color: #d4edda;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #28a745;
            margin: 1rem 0;
        }
        .prediction-moderate {
            background-color: #fff3cd;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #ffc107;
            margin: 1rem 0;
        }
        .prediction-high {
            background-color: #f8d7da;
            padding: 1.5rem;
            border-radius: 0.5rem;
            border-left: 4px solid #dc3545;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("# 🎓 University Student Stress Predictor")
st.markdown("**Predict your stress level based on lifestyle and academic factors**")
st.divider()

# Sidebar for navigation
st.sidebar.markdown("# Navigation")
page = st.sidebar.radio("Select a page:", ["Predict My Stress", "Model Information", "Tips & Resources"])

# ============================================================================
# PAGE 1: PREDICT MY STRESS
# ============================================================================
if page == "Predict My Stress":
    st.markdown("## Enter Your Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Personal Information")
        age = st.number_input("Age", min_value=18, max_value=50, value=21, step=1)
        
        degree = st.selectbox(
            "Degree Type",
            ["licence", "cycle d'ingénieur", "mastère", "préparatoire intégrée", 
             "doctorat", "médecine", "pharmacie", "Bachelor degree at TBS"]
        )
        
        year = st.selectbox("Year of Study", ["1st", "2nd", "3rd", "4th", "5th"])
        
        major = st.text_input("Major/Field of Study", 
                             placeholder="e.g., Psychology, IT, Medicine")
    
    with col2:
        st.markdown("### Lifestyle Factors")
        sleep = st.select_slider(
            "Average Sleep Per Night",
            options=["Less than 5 hours", "5–6 hours", "7–8 hours", "More than 8 hours"],
            value="7–8 hours"
        )
        
        screen = st.select_slider(
            "Daily Screen Time (excluding study)",
            options=["Less than 2 hours", "2–4 hours", "4–6 hours", "More than 6 hours"],
            value="4–6 hours"
        )
        
        exercise = st.radio("Regular Physical Activity", ["Yes", "No"], horizontal=True)
        exercise = "yes" if exercise == "Yes" else "no"
        
        caffeine = st.slider("Caffeinated Drinks Per Day", 0, 3, 1)
    
    st.divider()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### Academic Information")
        study = st.select_slider(
            "Study Hours Per Week (outside class)",
            options=["Less than 10 hours", "10–20 hours", "20–30 hours", "More than 30 hours"],
            value="10–20 hours"
        )
        
        exam = st.radio("Exams in Next 2 Weeks?", ["No", "Yes"], horizontal=True)
        exam = "yes" if exam == "Yes" else "no"
    
    with col4:
        st.markdown("### Workload Assessment")
        workload = st.select_slider(
            "Current Academic Workload",
            options=["low", "moderate", "high"],
            value="moderate"
        )
    
    st.divider()
    
    # Prediction button
    if st.button("🔮 Predict My Stress Level", use_container_width=True, type="primary"):
        
        if not major:
            st.error("❌ Please enter your major/field of study")
        else:
            # Make prediction
            result = predict_stress_level(
                age=age,
                degree=degree,
                year_of_study=year,
                major=major,
                sleep_hours_category=sleep,
                screen_time_category=screen,
                physical_activity=exercise,
                caffeine_drinks_category=str(caffeine),
                study_hours_category=study,
                exam_soon=exam,
                workload_level=workload.lower()
            )
            
            if 'error' in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                stress_level = result['predicted_stress_level']
                category = result['stress_category']
                
                # Display result in different colors based on stress level
                if stress_level < 4:
                    st.markdown(f"""
                    <div class="prediction-low">
                        <h3>✅ Low Stress Level: {stress_level:.2f}/10</h3>
                        <p>You're managing well! Continue with your current habits and maintain your healthy routines.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    color = "green"
                    emoji = "😊"
                    
                elif stress_level < 7:
                    st.markdown(f"""
                    <div class="prediction-moderate">
                        <h3>⚠️ Moderate Stress Level: {stress_level:.2f}/10</h3>
                        <p>You're experiencing some stress but it's manageable. Consider making small adjustments to reduce pressure.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    color = "orange"
                    emoji = "😐"
                    
                else:
                    st.markdown(f"""
                    <div class="prediction-high">
                        <h3>🚨 High Stress Level: {stress_level:.2f}/10</h3>
                        <p>You're experiencing significant stress. Consider seeking support from academic advisors or counseling services.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    color = "red"
                    emoji = "😟"
                
                # Beautiful gauge chart
                st.markdown("### Stress Level Visualization")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=stress_level,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Your Stress Level (1-10 Scale)", 'font': {'size': 20}},
                    delta={'reference': 5, 'prefix': "vs Average: "},
                    gauge={
                        'axis': {'range': [0, 10], 'tickwidth': 1},
                        'bar': {'color': color, 'thickness': 0.7},
                        'steps': [
                            {'range': [0, 3], 'color': "#90EE90"},
                            {'range': [3, 7], 'color': "#FFE4B5"},
                            {'range': [7, 10], 'color': "#FFB6C6"}
                        ],
                        'threshold': {
                            'line': {'color': "darkred", 'width': 3},
                            'thickness': 0.75,
                            'value': 9
                        }
                    },
                    number={'suffix': "/10", 'font': {'size': 30}}
                ))
                
                fig.update_layout(
                    height=400,
                    font={'size': 12},
                    margin=dict(l=0, r=0, t=50, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations based on stress level
                st.markdown("### Personalized Recommendations")
                
                col_rec1, col_rec2 = st.columns(2)
                
                with col_rec1:
                    st.markdown("**🎯 Immediate Actions:**")
                    if stress_level < 4:
                        st.markdown("""
                        - ✅ Maintain your current sleep schedule
                        - ✅ Keep exercising regularly
                        - ✅ Monitor caffeine intake
                        """)
                    elif stress_level < 7:
                        st.markdown("""
                        - 🟡 Try to increase sleep to 7-8 hours
                        - 🟡 Add 30 minutes of exercise daily
                        - 🟡 Reduce caffeine to 1-2 drinks/day
                        """)
                    else:
                        st.markdown("""
                        - 🔴 Seek support immediately
                        - 🔴 Talk to academic advisor
                        - 🔴 Consider counseling services
                        """)
                
                with col_rec2:
                    st.markdown("**💪 Long-term Strategies:**")
                    if stress_level < 4:
                        st.markdown("""
                        - Help other students
                        - Mentor peers
                        - Share your strategies
                        """)
                    elif stress_level < 7:
                        st.markdown("""
                        - Join study groups
                        - Practice time management
                        - Build support network
                        """)
                    else:
                        st.markdown("""
                        - Develop time management skills
                        - Create realistic workload plan
                        - Practice relaxation techniques
                        """)
                
                # Show factor breakdown
                st.markdown("### Your Stress Factors")
                factors = {
                    "Academic Workload": "🎓 " + workload,
                    "Sleep Quality": f"😴 {sleep}",
                    "Screen Time": f"📱 {screen}",
                    "Physical Activity": "🏃 " + ("Yes" if exercise == "yes" else "No"),
                    "Upcoming Exams": "📚 " + ("Yes" if exam == "yes" else "No"),
                    "Caffeine Intake": f"☕ {caffeine} drinks/day"
                }
                
                for factor, value in factors.items():
                    col_f1, col_f2 = st.columns([1, 1])
                    with col_f1:
                        st.text(factor)
                    with col_f2:
                        st.text(value)

# ============================================================================
# PAGE 2: MODEL INFORMATION
# ============================================================================
elif page == "Model Information":
    st.markdown("## About This Model")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Dataset Size", "545 Students", "+0")
        st.metric("Features Used", "11 Predictors", "+0")
    
    with col2:
        st.metric("Model Accuracy (R²)", "0.5109", "51% of variance")
        st.metric("Average Error", "±1.42", "points on scale")
    
    with col3:
        st.metric("Train/Test Split", "80% / 20%", "436 / 109 samples")
    
    st.divider()
    
    st.markdown("### Key Statistics")
    df_stats = pd.DataFrame({
        "Metric": ["Average Stress Level", "Minimum Stress", "Maximum Stress", "Standard Deviation"],
        "Value": ["5.89/10", "1/10", "10/10", "2.65"]
    })
    st.dataframe(df_stats, use_container_width=True)
    
    st.divider()
    
    st.markdown("### Top Stress Factors (Feature Importance)")
    
    factors = ["Academic Workload", "Major/Field", "Sleep Hours", "Upcoming Exams", "Age"]
    importance = [35.9, 11.5, 11.4, 9.0, 7.9]
    
    fig = go.Figure(data=[
        go.Bar(
            y=factors,
            x=importance,
            orientation='h',
            marker=dict(
                color=importance,
                colorscale='Reds',
                showscale=False
            ),
            text=[f"{imp:.1f}%" for imp in importance],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Impact of Different Factors on Stress Level",
        xaxis_title="Importance Score (%)",
        yaxis_title="Factors",
        height=400,
        showlegend=False,
        margin=dict(l=150)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.markdown("### Model Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Model Comparison:**")
        comparison_data = {
            "Model": ["Linear Regression", "Random Forest", "Gradient Boosting"],
            "R² Score": [0.5109, 0.3875, 0.3739],
            "MAE": [1.4216, 1.5899, 1.6531]
        }
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
    
    with col2:
        st.markdown("**Why Linear Regression?**")
        st.markdown("""
        - ✅ Best test performance (R² = 0.5109)
        - ✅ Better generalization
        - ✅ No overfitting (unlike Random Forest)
        - ✅ More interpretable
        - ✅ Consistent cross-validation scores
        """)
    
    st.divider()
    
    st.markdown("### Technical Details")
    st.markdown("""
    **Data Preprocessing:**
    - Removed timestamp column
    - Encoded categorical variables (age, degree, year, major)
    - Mapped categorical ranges to numerical values
    - Applied StandardScaler for feature normalization
    
    **Model Training:**
    - Algorithm: Linear Regression (scikit-learn)
    - Train samples: 436
    - Test samples: 109
    - Cross-validation: 5-fold
    
    **Performance Metrics:**
    - R² Score: 0.5109 (explains 51% of variance)
    - MAE: 1.4216 (average error)
    - RMSE: 1.7720 (penalizes larger errors)
    """)

# ============================================================================
# PAGE 3: TIPS & RESOURCES
# ============================================================================
elif page == "Tips & Resources":
    st.markdown("## Stress Management Tips")
    
    st.markdown("### 😴 Sleep is Your Foundation")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Why Sleep Matters:**
        - Sleep deprivation is the #2 stress factor in our model
        - 7-8 hours is the sweet spot
        - Improves focus and decision-making
        - Boosts immune system
        """)
    
    with col2:
        st.markdown("""
        **Sleep Tips:**
        - Set consistent bed time
        - Avoid screens 30 min before bed
        - Keep bedroom cool and dark
        - Limit caffeine after 2 PM
        - Try relaxation techniques
        """)
    
    st.divider()
    
    st.markdown("### 🎓 Manage Your Workload")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Academic Workload is #1 Stress Factor:**
        - 35.9% of all stress comes from workload
        - Different majors have different stress levels
        - Plan ahead for exams
        - Break large tasks into smaller ones
        """)
    
    with col2:
        st.markdown("""
        **Workload Management:**
        - Use a planner or calendar
        - Prioritize important tasks
        - Delegate when possible
        - Communicate with professors
        - Take regular breaks
        """)
    
    st.divider()
    
    st.markdown("### 🏃 Exercise is Powerful")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Benefits of Exercise:**
        - Reduces physical tension
        - Improves mental clarity
        - Boosts mood with endorphins
        - Improves sleep quality
        - Builds resilience
        """)
    
    with col2:
        st.markdown("""
        **Exercise Recommendations:**
        - 30 minutes daily is ideal
        - Mix cardio and strength training
        - Find activities you enjoy
        - Exercise with friends
        - Morning exercise energizes day
        """)
    
    st.divider()
    
    st.markdown("### ☕ Caffeine: Moderation is Key")
    st.markdown("""
    - **Optimal intake:** 1-2 drinks per day
    - **Peak effect:** 30 minutes after consumption
    - **Half-life:** 5 hours (affects sleep)
    - **Avoid after:** 2 PM
    - **Types:** Coffee, tea, energy drinks, soda
    """)
    
    st.divider()
    
    st.markdown("### 📱 Screen Time Management")
    st.markdown("""
    **Recommended Limits:**
    - Academic work: As needed
    - Social media: 1-2 hours per day
    - Total screen time: 4-6 hours outside class
    - Before bed: 0 hours (avoid 30 min before sleep)
    
    **Tips:**
    - Use blue light filters
    - Take 20-20-20 breaks (20 sec, 20 ft, every 20 min)
    - Turn off notifications
    - Practice digital detox weekends
    """)
    
    st.divider()
    
    st.markdown("### 🆘 When to Seek Help")
    
    st.warning("""
    **Contact your university if you experience:**
    - Persistent feeling of being overwhelmed
    - Difficulty concentrating or sleeping
    - Loss of interest in activities
    - Physical symptoms (headaches, stomach issues)
    - Thoughts of self-harm
    
    **Resources:**
    - 📞 Student Counseling Services
    - 📚 Academic Advising
    - 🏥 University Health Center
    - 💬 Peer Support Groups
    - 🌐 Mental Health Hotlines
    """)
    
    st.divider()
    
    st.markdown("### 📊 Stress Scale Reference")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Low Stress (1-3)**
        
        ✅ You're doing great!
        - Maintain routines
        - Help others
        - Enjoy the balance
        """)
    
    with col2:
        st.markdown("""
        **Moderate Stress (4-7)**
        
        ⚠️ Watch and adjust
        - Make small changes
        - Monitor workload
        - Seek support if needed
        """)
    
    with col3:
        st.markdown("""
        **High Stress (8-10)**
        
        🚨 Take action now
        - Reach out for help
        - Reduce workload
        - Prioritize self-care
        """)

# Footer
st.divider()
st.markdown("""
---
**Stress Predictor v1.0** | Built with ❤️ for University Students  
*This model is based on survey data from 545 university students.*  
**Disclaimer:** This tool is for informational purposes only and should not replace professional mental health advice.
""")
