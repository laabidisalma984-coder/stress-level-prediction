import pandas as pd
import numpy as np
import joblib
import os
import warnings

warnings.filterwarnings('ignore')

# ==================== MODEL PERSISTENCE & PREDICTION INTERFACE ====================
"""
Stress Level Prediction System v2.0
Loads the pre-trained ensemble model pipeline for high-performance predictions.
"""

MODEL_PATH = 'stress_model_v2.joblib'

def load_prediction_system():
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    return None

# Global pipeline instance
pipeline = load_prediction_system()

# Define mappings for input categories to midpoints (same as training)
sleep_mapping = {'Less than 5 hours': 4, '5–6 hours': 5.5, '7–8 hours': 7.5, 'More than 8 hours': 9}
screen_mapping = {'Less than 2 hours': 1, '2–4 hours': 3, '4–6 hours': 5, 'More than 6 hours': 7}
study_mapping = {'Less than 10 hours': 7, '10–20 hours': 15, '20–30 hours': 25, 'More than 30 hours': 35}
workload_mapping = {'low': 1, 'moderate': 2, 'high': 3}

def predict_stress_level(age, degree, year_of_study, major, sleep_hours_category, 
                        screen_time_category, physical_activity, caffeine_drinks_category,
                        study_hours_category, exam_soon, workload_level):
    """
    Predict stress level for a student based on their characteristics
    Using the enhanced Ensemble Model (v2.0)
    """
    if pipeline is None:
        return {"error": "Prediction model not found. Please run stress_prediction_model.py first."}
    
    try:
        # 1. Map inputs to raw features
        sleep_hours = sleep_mapping.get(sleep_hours_category, 6)
        screen_time = screen_mapping.get(screen_time_category, 4)
        physical_act = 1 if physical_activity.lower() == 'yes' else 0
        caffeine = 3 if caffeine_drinks_category == '3 or more' else float(caffeine_drinks_category)
        study_hours = study_mapping.get(study_hours_category, 20)
        exam = 1 if exam_soon.lower() == 'yes' else 0
        workload = workload_mapping.get(workload_level.lower(), 2)
        
        # 2. Create feature dictionary for DataFrame (ensures column order)
        input_data = {
            "what's your age": [int(age)],
            "what's your degree": [degree],
            "what is your year of studies": [year_of_study],
            "what is your major": [major],
            "Sleep_Hours": [sleep_hours],
            "Screen_Time_Hours": [screen_time],
            "Physical_Activity": [physical_act],
            "Caffeine_Drinks": [caffeine],
            "Study_Hours_Per_Week": [study_hours],
            "Exam_In_Two_Weeks": [exam],
            "Academic_Workload": [workload]
        }
        
        # 3. Add Engineered Features (must match training exactly)
        input_data['Workload_Study_Interaction'] = [workload * study_hours]
        input_data['Sleep_Screen_Ratio'] = [sleep_hours / (screen_time + 1)]
        input_data['Stress_Multiplier'] = [workload * (exam + 1)]
        input_data['Lifestyle_Score'] = [(sleep_hours + physical_act * 2) - (caffeine * 0.5)]
        
        df_input = pd.DataFrame(input_data)
        
        # 4. Predict using the pipeline (handles scaling and encoding automatically)
        stress_prediction = pipeline.predict(df_input)[0]
        stress_prediction = max(1, min(10, stress_prediction))
        
        return {
            "predicted_stress_level": round(stress_prediction, 2),
            "stress_category": "Low" if stress_prediction < 4 else ("Moderate" if stress_prediction < 7 else "High"),
            "confidence": "High"
        }
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("\n===========================================")
    print("🎓 Stress Level Prediction System CLI v2.0")
    print("===========================================\n")
    print("Since the web dashboard is currently unavailable, use this CLI to test the model.\n")
    
    try:
        age = input("Age (e.g., 21): ")
        degree = input("Degree (e.g., licence, master): ")
        year = input("Year of study (e.g., 1st, 2nd, 3rd): ")
        major = input("Major (e.g., Psychology, IT): ")
        sleep = input("Sleep Hours (Less than 5 hours/5–6 hours/7–8 hours/More than 8 hours): ")
        screen = input("Screen Time (Less than 2 hours/2–4 hours/4–6 hours/More than 6 hours): ")
        phys = input("Physical Activity (yes/no): ")
        caf = input("Caffeine Drinks per day (0/1/2/3 or more): ")
        study = input("Study Hours per week (Less than 10 hours/10–20 hours/20–30 hours/More than 30 hours): ")
        exam = input("Exams in next 2 weeks? (yes/no): ")
        workload = input("Academic Workload (low/moderate/high): ")
        
        print("\n⏳ Predicting...")
        res = predict_stress_level(age, degree, year, major, sleep, screen, phys, caf, study, exam, workload)
        
        if "error" in res:
            print(f"❌ Error: {res['error']}")
        else:
            print(f"\n✅ Predicted Stress Level: {res['predicted_stress_level']}/10")
            print(f"📊 Stress Category: {res['stress_category']}")
            
    except KeyboardInterrupt:
        print("\nExiting CLI.")
