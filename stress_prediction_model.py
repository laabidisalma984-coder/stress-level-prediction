import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# ==================== DATA LOADING & EXPLORATION ====================
print("=" * 60)
print("STRESS LEVEL PREDICTION MODEL FOR UNIVERSITY STUDENTS")
print("=" * 60)

# Load the dataset
df = pd.read_csv('dataset_ml_500.csv')
print(f"\nDataset shape: {df.shape}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nColumn names:")
print(df.columns.tolist())
print(f"\nData types:")
print(df.dtypes)
print(f"\nMissing values:")
print(df.isnull().sum())

# ==================== DATA PREPROCESSING ====================
print("\n" + "=" * 60)
print("DATA PREPROCESSING")
print("=" * 60)

# Create a copy for processing
df_processed = df.copy()

# Drop timestamp column (not useful for prediction)
df_processed = df_processed.drop('Timestamp', axis=1)

# Rename columns for clarity (removing extra spaces)
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

# Apply mappings
df_processed['Sleep_Hours'] = df_processed['How many hours do you sleep on average per night?'].map(sleep_mapping)
df_processed['Screen_Time_Hours'] = df_processed['How many hours do you spend on screens per day (excluding academic work)?'].map(screen_mapping)
df_processed['Physical_Activity'] = df_processed['Do you engage in regular physical activity ?'].map({'yes': 1, 'no': 0})

# Handle caffeine drinks - convert to numeric, handling "3 or more" case
caffeine_col = 'How many caffeinated drinks (coffee, tea, energy drinks) do you consume per day?'
df_processed['Caffeine_Drinks'] = df_processed[caffeine_col].apply(lambda x: 3 if x == '3 or more' else float(x))

df_processed['Study_Hours_Per_Week'] = df_processed['How many hours do you study per week outside of class?'].map(study_mapping)
df_processed['Exam_In_Two_Weeks'] = df_processed['do u have exams in the next two weeks'].map({'yes': 1, 'no': 0})
df_processed['Academic_Workload'] = df_processed['How would you rate your current academic workload?'].map(workload_mapping)

# Target variable: Stress Level
df_processed['Stress_Level'] = df_processed['On a scale from 1 to 10, how would you rate your current stress level?'].astype(float)

# Encode categorical variables
le_age = LabelEncoder()
le_degree = LabelEncoder()
le_year = LabelEncoder()
le_major = LabelEncoder()

df_processed['Age_Encoded'] = le_age.fit_transform(df_processed['what\'s your age'].astype(str))
df_processed['Degree_Encoded'] = le_degree.fit_transform(df_processed['what\'s your degree'])
df_processed['Year_Encoded'] = le_year.fit_transform(df_processed['what is your year of studies'])
df_processed['Major_Encoded'] = le_major.fit_transform(df_processed['what is your major'])

# Select features for the model
features = [
    'Age_Encoded', 'Degree_Encoded', 'Year_Encoded', 'Major_Encoded',
    'Sleep_Hours', 'Screen_Time_Hours', 'Physical_Activity',
    'Caffeine_Drinks', 'Study_Hours_Per_Week', 'Exam_In_Two_Weeks',
    'Academic_Workload'
]

X = df_processed[features].copy()
y = df_processed['Stress_Level'].copy()

print(f"\nFeatures used in the model:")
for i, feat in enumerate(features, 1):
    print(f"  {i}. {feat}")

print(f"\nTarget variable (Stress Level) statistics:")
print(f"  Min: {y.min()}, Max: {y.max()}, Mean: {y.mean():.2f}, Std: {y.std():.2f}")

# ==================== FEATURE SCALING ====================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_scaled = pd.DataFrame(X_scaled, columns=features)

# ==================== TRAIN-TEST SPLIT ====================
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"\nTrain set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# ==================== MODEL TRAINING ====================
print("\n" + "=" * 60)
print("MODEL TRAINING")
print("=" * 60)

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5)
}

results = {}

for name, model in models.items():
    print(f"\nTraining {name}...")
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    # Calculate metrics
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    train_mse = mean_squared_error(y_train, y_pred_train)
    test_mse = mean_squared_error(y_test, y_pred_test)
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    
    results[name] = {
        'model': model,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_mse': train_mse,
        'test_mse': test_mse,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'y_pred_test': y_pred_test
    }
    
    print(f"  Train R² Score: {train_r2:.4f}")
    print(f"  Test R² Score: {test_r2:.4f}")
    print(f"  Train MAE: {train_mae:.4f}")
    print(f"  Test MAE: {test_mae:.4f}")
    print(f"  Cross-Validation R² (mean ± std): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ==================== FEATURE IMPORTANCE ====================
print("\n" + "=" * 60)
print("FEATURE IMPORTANCE (Random Forest)")
print("=" * 60)

rf_model = results['Random Forest']['model']
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10).to_string(index=False))

# ==================== VISUALIZATIONS ====================
print("\n" + "=" * 60)
print("GENERATING VISUALIZATIONS")
print("=" * 60)

# 1. Feature Importance Plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Feature Importance
ax = axes[0, 0]
top_features = feature_importance.head(10)
ax.barh(top_features['Feature'], top_features['Importance'], color='steelblue')
ax.set_xlabel('Importance Score')
ax.set_title('Top 10 Feature Importance (Random Forest)')
ax.invert_yaxis()

# Model Comparison - R² Scores
ax = axes[0, 1]
model_names = list(results.keys())
test_r2_scores = [results[m]['test_r2'] for m in model_names]
colors = ['#2ecc71', '#3498db', '#e74c3c']
bars = ax.bar(model_names, test_r2_scores, color=colors, alpha=0.7, edgecolor='black')
ax.set_ylabel('R² Score')
ax.set_title('Model Comparison - Test R² Score')
ax.set_ylim([0, 1])
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.4f}', ha='center', va='bottom')

# Predictions vs Actual (Best Model - Random Forest)
ax = axes[1, 0]
best_model_name = 'Random Forest'
y_pred = results[best_model_name]['y_pred_test']
ax.scatter(y_test, y_pred, alpha=0.6, color='purple', edgecolors='black')
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
ax.set_xlabel('Actual Stress Level')
ax.set_ylabel('Predicted Stress Level')
ax.set_title(f'{best_model_name}: Predictions vs Actual')
ax.grid(True, alpha=0.3)

# Residuals
ax = axes[1, 1]
residuals = y_test - y_pred
ax.scatter(y_pred, residuals, alpha=0.6, color='orange', edgecolors='black')
ax.axhline(y=0, color='r', linestyle='--', lw=2)
ax.set_xlabel('Predicted Stress Level')
ax.set_ylabel('Residuals')
ax.set_title(f'{best_model_name}: Residuals Plot')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('stress_prediction_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: stress_prediction_analysis.png")

# ==================== SUMMARY REPORT ====================
print("\n" + "=" * 60)
print("MODEL SUMMARY REPORT")
print("=" * 60)

best_model_name = max(results, key=lambda x: results[x]['test_r2'])
best_model_info = results[best_model_name]

print(f"\n🏆 BEST MODEL: {best_model_name}")
print(f"   Test R² Score: {best_model_info['test_r2']:.4f}")
print(f"   Test MAE: {best_model_info['test_mae']:.4f}")
print(f"   Test RMSE: {np.sqrt(best_model_info['test_mse']):.4f}")
print(f"   Cross-Val Score: {best_model_info['cv_mean']:.4f} ± {best_model_info['cv_std']:.4f}")

print(f"\nKey Insights:")
print(f"  • The model explains {best_model_info['test_r2']*100:.2f}% of stress level variance")
print(f"  • Average prediction error: ±{best_model_info['test_mae']:.2f} points on the stress scale")
print(f"  • Top 3 stress factors:")
for i, row in feature_importance.head(3).iterrows():
    print(f"    - {row['Feature']}: {row['Importance']:.4f}")

print("\n" + "=" * 60)
print("MODEL TRAINING COMPLETE!")
print("=" * 60)
