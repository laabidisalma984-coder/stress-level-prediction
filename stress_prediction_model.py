import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.linear_model import Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import lightgbm as lgb
import joblib
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ==================== DATA LOADING & PREPROCESSING ====================
print("\n" + "=" * 60)
print("ENHANCED STRESS LEVEL PREDICTION MODEL")
print("=" * 60)

# Load the extended dataset
try:
    df = pd.read_csv('dataset_ml_extended.csv')
    print(f"\nDataset shape: {df.shape}")
except FileNotFoundError:
    print("Error: Could not find dataset_ml_extended.csv. Please ensure it's in the same directory.")
    exit()

print("DATA PREPROCESSING & FEATURE ENGINEERING")
print("=" * 60)

# Create a copy for processing
df_processed = df.copy()

# Drop timestamp column
if 'Timestamp' in df_processed.columns:
    df_processed = df_processed.drop('Timestamp', axis=1)

# Clean column names
df_processed.columns = df_processed.columns.str.strip()

# Create a mapping for sleep hours
sleep_mapping = {
    'Less than 5 hours': 4,
    '5–6 hours': 5.5,
    '7–8 hours': 7.5,
    'More than 8 hours': 9
}

# Create a mapping for screen time
screen_mapping = {
    'Less than 2 hours': 1,
    '2–4 hours': 3,
    '4–6 hours': 5,
    'More than 6 hours': 7
}

# Create a mapping for study hours
study_mapping = {
    'Less than 10 hours': 7,
    '10–20 hours': 15,
    '20–30 hours': 25,
    'More than 30 hours': 35
}

# Create a mapping for academic workload
workload_mapping = {
    'low': 1,
    'moderate': 2,
    'high': 3
}

# Apply mappings (ordinal features)
df_processed['Sleep_Hours'] = df_processed['How many hours do you sleep on average per night?'].map(sleep_mapping)
df_processed['Screen_Time_Hours'] = df_processed['How many hours do you spend on screens per day (excluding academic work)?'].map(screen_mapping)
df_processed['Physical_Activity'] = df_processed['Do you engage in regular physical activity ?'].map({'yes': 1, 'no': 0})

caffeine_col = 'How many caffeinated drinks (coffee, tea, energy drinks) do you consume per day?'
df_processed['Caffeine_Drinks'] = df_processed[caffeine_col].apply(lambda x: 3 if x == '3 or more' else float(x))

df_processed['Study_Hours_Per_Week'] = df_processed['How many hours do you study per week outside of class?'].map(study_mapping)
df_processed['Exam_In_Two_Weeks'] = df_processed['do u have exams in the next two weeks'].map({'yes': 1, 'no': 0})
df_processed['Academic_Workload'] = df_processed['How would you rate your current academic workload?'].map(workload_mapping)

# Target variable: Stress Level
target_col = 'On a scale from 1 to 10, how would you rate your current stress level?'
df_processed['Stress_Level'] = df_processed[target_col].astype(float)

# ==================== ADVANCED FEATURE ENGINEERING ====================

# 1. Interaction Features
df_processed['Workload_Study_Interaction'] = df_processed['Academic_Workload'] * df_processed['Study_Hours_Per_Week']
df_processed['Sleep_Screen_Ratio'] = df_processed['Sleep_Hours'] / (df_processed['Screen_Time_Hours'] + 1)
df_processed['Stress_Multiplier'] = df_processed['Academic_Workload'] * (df_processed['Exam_In_Two_Weeks'] + 1)

# 2. Derived Lifestyle Score
df_processed['Lifestyle_Score'] = (df_processed['Sleep_Hours'] + df_processed['Physical_Activity'] * 2) - (df_processed['Caffeine_Drinks'] * 0.5)

# Define feature groups
categorical_features = ["what's your degree", 'what is your year of studies', 'what is your major']
numerical_features = [
    "what's your age", 'Sleep_Hours', 'Screen_Time_Hours', 'Physical_Activity',
    'Caffeine_Drinks', 'Study_Hours_Per_Week', 'Exam_In_Two_Weeks', 'Academic_Workload',
    'Workload_Study_Interaction', 'Sleep_Screen_Ratio', 'Stress_Multiplier', 'Lifestyle_Score'
]

X = df_processed[categorical_features + numerical_features]
y = df_processed['Stress_Level']

# ==================== PIPELINE DEFINITION ====================

# Preprocessing for categorical data: OneHotEncoding
# Preprocessing for numerical data: StandardScaling
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ])

# ==================== TRAIN-TEST SPLIT ====================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==================== MODEL DEFINITION & HYPERPARAMETER TUNING ====================
print("\n" + "=" * 60)
print("MODEL TRAINING & OPTIMIZATION")
print("=" * 60)

def get_best_model(name, regressor, param_dist):
    print(f"\nOptimizing {name}...")
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', regressor)])
    
    # Randomized Search
    search = RandomizedSearchCV(
        pipeline, param_distributions=param_dist, 
        n_iter=20, cv=5, scoring='r2', n_jobs=-1, random_state=42
    )
    search.fit(X_train, y_train)
    print(f"  Best CV R² Score: {search.best_score_:.4f}")
    return search.best_estimator_

# Hyperparameters for RandomizedSearch
params_rf = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__max_depth': [5, 10, 15, None],
    'regressor__min_samples_split': [2, 5, 10],
    'regressor__min_samples_leaf': [1, 2, 4]
}

params_xgb = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__learning_rate': [0.01, 0.05, 0.1],
    'regressor__max_depth': [3, 5, 7],
    'regressor__subsample': [0.8, 0.9, 1.0]
}

params_lgb = {
    'regressor__n_estimators': [100, 200, 300],
    'regressor__learning_rate': [0.01, 0.05, 0.1],
    'regressor__num_leaves': [20, 31, 40],
    'regressor__feature_fraction': [0.8, 0.9, 1.0]
}

# Optimize individual models
best_rf = get_best_model('Random Forest', RandomForestRegressor(random_state=42), params_rf)
best_xgb = get_best_model('XGBoost', xgb.XGBRegressor(random_state=42), params_xgb)
best_lgb = get_best_model('LightGBM', lgb.LGBMRegressor(random_state=42, verbosity=-1), params_lgb)

# Create Ensemble (Voting Regressor)
print("\nCreating Voting Ensemble...")
ensemble = VotingRegressor(estimators=[
    ('rf', best_rf.named_steps['regressor']),
    ('xgb', best_xgb.named_steps['regressor']),
    ('lgb', best_lgb.named_steps['regressor']),
    ('ridge', Ridge(alpha=1.0))
])

# Final Pipeline with Ensemble
final_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('ensemble', ensemble)
])

final_pipeline.fit(X_train, y_train)

# ==================== EVALUATION ====================
y_pred = final_pipeline.predict(X_test)
test_r2 = r2_score(y_test, y_pred)
test_mae = mean_absolute_error(y_test, y_pred)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n" + "=" * 60)
print("FINAL ENSEMBLE PERFORMANCE")
print("=" * 60)
print(f"Test R² Score: {test_r2:.4f}")
print(f"Test MAE: {test_mae:.4f}")
print(f"Test RMSE: {test_rmse:.4f}")

# Cross-validation
cv_scores = cross_val_score(final_pipeline, X, y, cv=5, scoring='r2')
print(f"Cross-Validation R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ==================== MODEL EXPORT ====================
print("\n" + "=" * 60)
print("EXPORTING MODEL")
print("=" * 60)

# Export the entire pipeline
model_filename = 'stress_model_v2.joblib'
joblib.dump(final_pipeline, model_filename)
print(f"DONE: Model and Preprocessing saved to: {model_filename}")

# ==================== VISUALIZATIONS ====================
# Predictions vs Actual
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6, color='teal', edgecolors='black')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual Stress Level')
plt.ylabel('Predicted Stress Level')
plt.title('Ensemble Model: Predictions vs Actual')
plt.grid(True, alpha=0.3)
plt.savefig('stress_prediction_analysis_v2.png', dpi=300, bbox_inches='tight')

print("DONE: Saved: stress_prediction_analysis_v2.png")

# Confusion Matrix (Rounded Predictions)
from sklearn.metrics import confusion_matrix
y_pred_rounded = np.clip(np.round(y_pred), 1, 10).astype(int)
y_test_int = y_test.astype(int)
labels = range(1, 11)
cm = confusion_matrix(y_test_int, y_pred_rounded, labels=labels)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
plt.xlabel('Predicted Stress Level', fontsize=12, fontweight='bold')
plt.ylabel('Actual Stress Level', fontsize=12, fontweight='bold')
plt.title('Confusion Matrix (Rounded Predictions)', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300)
print("DONE: Saved: confusion_matrix.png")

print("\n" + "=" * 60)
print("ENHANCED TRAINING COMPLETE!")
print("=" * 60)
