import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
import pickle
import os

# ==================== MODEL PERSISTENCE & PREDICTION INTERFACE ====================
"""
Stress Level Prediction System
Provides functions to save trained models and make predictions on new student data
"""

# Load the original dataset for fitting encoders and scalers
df = pd.read_csv('dataset_ml_500.csv')
df_processed = df.copy()
df_processed = df_processed.drop('Timestamp', axis=1)
df_processed.columns = df_processed.columns.str.strip()

# Define mappings
sleep_mapping = {
    'Less than 5 hours': 4,
    '5–6 hours': 5.5,
    '7–8 hours': 7.5,
    'More than 8 hours': 9
}

screen_mapping = {
    'Less than 2 hours': 1,
    '2–4 hours': 3,
    '4–6 hours': 5,
    'More than 6 hours': 7
}

study_mapping = {
    'Less than 10 hours': 7,
    '10–20 hours': 15,
    '20–30 hours': 25,
    'More than 30 hours': 35
}

workload_mapping = {
    'low': 1,
    'moderate': 2,
    'high': 3
}

# Prepare data for model training
df_processed['Sleep_Hours'] = df_processed['How many hours do you sleep on average per night?'].map(sleep_mapping)
df_processed['Screen_Time_Hours'] = df_processed['How many hours do you spend on screens per day (excluding academic work)?'].map(screen_mapping)
df_processed['Physical_Activity'] = df_processed['Do you engage in regular physical activity ?'].map({'yes': 1, 'no': 0})

caffeine_col = 'How many caffeinated drinks (coffee, tea, energy drinks) do you consume per day?'
df_processed['Caffeine_Drinks'] = df_processed[caffeine_col].apply(lambda x: 3 if x == '3 or more' else float(x))

df_processed['Study_Hours_Per_Week'] = df_processed['How many hours do you study per week outside of class?'].map(study_mapping)
df_processed['Exam_In_Two_Weeks'] = df_processed['do u have exams in the next two weeks'].map({'yes': 1, 'no': 0})
df_processed['Academic_Workload'] = df_processed['How would you rate your current academic workload?'].map(workload_mapping)
df_processed['Stress_Level'] = df_processed['On a scale from 1 to 10, how would you rate your current stress level?'].astype(float)

# Fit encoders
le_age = LabelEncoder()
le_degree = LabelEncoder()
le_year = LabelEncoder()
le_major = LabelEncoder()

df_processed['Age_Encoded'] = le_age.fit_transform(df_processed['what\'s your age'].astype(str))
df_processed['Degree_Encoded'] = le_degree.fit_transform(df_processed['what\'s your degree'])
df_processed['Year_Encoded'] = le_year.fit_transform(df_processed['what is your year of studies'])
df_processed['Major_Encoded'] = le_major.fit_transform(df_processed['what is your major'])

features = [
    'Age_Encoded', 'Degree_Encoded', 'Year_Encoded', 'Major_Encoded',
    'Sleep_Hours', 'Screen_Time_Hours', 'Physical_Activity',
    'Caffeine_Drinks', 'Study_Hours_Per_Week', 'Exam_In_Two_Weeks',
    'Academic_Workload'
]

X = df_processed[features].copy()
y = df_processed['Stress_Level'].copy()

# Fit scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the best model (Linear Regression)
model = LinearRegression()
model.fit(X_scaled, y)

print("✓ Model trained and ready for predictions!")

# ==================== PREDICTION FUNCTION ====================
def predict_stress_level(age, degree, year_of_study, major, sleep_hours_category, 
                        screen_time_category, physical_activity, caffeine_drinks_category,
                        study_hours_category, exam_soon, workload_level):
    """
    Predict stress level for a student based on their characteristics
    
    Parameters:
    - age: Integer (e.g., 20)
    - degree: String ('licence', 'cycle d\'ingénieur', 'mastère', 'doctorat', 'médecine', 'pharmacie', etc.)
    - year_of_study: String ('1st', '2nd', '3rd', '4th', '5th')
    - major: String (student's major/field)
    - sleep_hours_category: String ('Less than 5 hours', '5–6 hours', '7–8 hours', 'More than 8 hours')
    - screen_time_category: String ('Less than 2 hours', '2–4 hours', '4–6 hours', 'More than 6 hours')
    - physical_activity: String ('yes' or 'no')
    - caffeine_drinks_category: String or Integer ('0', '1', '2', '3 or more', or integer 0-3)
    - study_hours_category: String ('Less than 10 hours', '10–20 hours', '20–30 hours', 'More than 30 hours')
    - exam_soon: String ('yes' or 'no')
    - workload_level: String ('low', 'moderate', 'high')
    
    Returns:
    - Dictionary with predicted stress level (1-10 scale) and explanation
    """
    
    try:
        # Encode age
        age_encoded = le_age.transform([str(age)])[0]
        
        # Encode degree
        if degree not in le_degree.classes_:
            return {"error": f"Unknown degree: {degree}. Try one of: {list(le_degree.classes_)}"}
        degree_encoded = le_degree.transform([degree])[0]
        
        # Encode year
        if year_of_study not in le_year.classes_:
            return {"error": f"Unknown year: {year_of_study}. Try one of: {list(le_year.classes_)}"}
        year_encoded = le_year.transform([year_of_study])[0]
        
        # Encode major
        if major not in le_major.classes_:
            return {"error": f"Unknown major: {major}. Try one of: {list(le_major.classes_)}"}
        major_encoded = le_major.transform([major])[0]
        
        # Map sleep hours
        if sleep_hours_category not in sleep_mapping:
            return {"error": f"Unknown sleep category: {sleep_hours_category}. Try one of: {list(sleep_mapping.keys())}"}
        sleep_hours = sleep_mapping[sleep_hours_category]
        
        # Map screen time
        if screen_time_category not in screen_mapping:
            return {"error": f"Unknown screen time category: {screen_time_category}. Try one of: {list(screen_mapping.keys())}"}
        screen_time = screen_mapping[screen_time_category]
        
        # Map physical activity
        physical_activity_encoded = 1 if physical_activity.lower() == 'yes' else 0
        
        # Map caffeine
        if isinstance(caffeine_drinks_category, str):
            caffeine_drinks = 3 if caffeine_drinks_category == '3 or more' else float(caffeine_drinks_category)
        else:
            caffeine_drinks = float(caffeine_drinks_category)
        
        # Map study hours
        if study_hours_category not in study_mapping:
            return {"error": f"Unknown study hours category: {study_hours_category}. Try one of: {list(study_mapping.keys())}"}
        study_hours = study_mapping[study_hours_category]
        
        # Map exam soon
        exam_soon_encoded = 1 if exam_soon.lower() == 'yes' else 0
        
        # Map workload
        if workload_level.lower() not in workload_mapping:
            return {"error": f"Unknown workload level: {workload_level}. Try one of: {list(workload_mapping.keys())}"}
        workload = workload_mapping[workload_level.lower()]
        
        # Create feature array
        features_list = np.array([[
            age_encoded, degree_encoded, year_encoded, major_encoded,
            sleep_hours, screen_time, physical_activity_encoded,
            caffeine_drinks, study_hours, exam_soon_encoded, workload
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features_list)
        
        # Make prediction
        stress_prediction = model.predict(features_scaled)[0]
        stress_prediction = max(1, min(10, stress_prediction))  # Clamp between 1-10
        
        return {
            "predicted_stress_level": round(stress_prediction, 2),
            "stress_category": "Low" if stress_prediction < 4 else ("Moderate" if stress_prediction < 7 else "High"),
            "confidence": "High" if 0.4 <= stress_prediction <= 9.6 else "Medium"
        }
        
    except Exception as e:
        return {"error": str(e)}


# ==================== EXAMPLE PREDICTIONS ====================
print("\n" + "=" * 60)
print("EXAMPLE STRESS PREDICTIONS")
print("=" * 60)

# Example 1: Well-rested student with low workload
print("\n📊 Example 1: Well-rested student with low stress factors")
result1 = predict_stress_level(
    age=21,
    degree='licence',
    year_of_study='2nd',
    major='Psychology',
    sleep_hours_category='7–8 hours',
    screen_time_category='2–4 hours',
    physical_activity='yes',
    caffeine_drinks_category='1',
    study_hours_category='10–20 hours',
    exam_soon='no',
    workload_level='low'
)
print(f"  Predicted Stress Level: {result1['predicted_stress_level']}/10 ({result1['stress_category']})")

# Example 2: Sleep-deprived student with high workload
print("\n📊 Example 2: Sleep-deprived student with high stress factors")
result2 = predict_stress_level(
    age=22,
    degree="cycle d'ingénieur",
    year_of_study='4th',
    major='IT',
    sleep_hours_category='Less than 5 hours',
    screen_time_category='More than 6 hours',
    physical_activity='no',
    caffeine_drinks_category='3 or more',
    study_hours_category='20–30 hours',
    exam_soon='yes',
    workload_level='high'
)
print(f"  Predicted Stress Level: {result2.get('predicted_stress_level', 'Error')}/10 ({result2.get('stress_category', 'N/A')})")
if 'error' in result2:
    print(f"  Error: {result2['error']}")

# Example 3: Average student
print("\n📊 Example 3: Average student with moderate factors")
result3 = predict_stress_level(
    age=20,
    degree='licence',
    year_of_study='1st',
    major='Law',
    sleep_hours_category='5–6 hours',
    screen_time_category='4–6 hours',
    physical_activity='yes',
    caffeine_drinks_category='1',
    study_hours_category='10–20 hours',
    exam_soon='yes',
    workload_level='moderate'
)
print(f"  Predicted Stress Level: {result3.get('predicted_stress_level', 'Error')}/10 ({result3.get('stress_category', 'N/A')})")
if 'error' in result3:
    print(f"  Error: {result3['error']}")

print("\n" + "=" * 60)
print("STRESS PREDICTION SYSTEM READY!")
print("=" * 60)
print("\nYou can use the predict_stress_level() function to make predictions.")
print("Check the function docstring for parameter options.")
