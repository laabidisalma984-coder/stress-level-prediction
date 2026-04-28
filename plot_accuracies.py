import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import xgboost as xgb
import lightgbm as lgb
import warnings

warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('dataset_ml_extended.csv')
X = df.iloc[:, 1:-1]
y = df.iloc[:, -1]

# Preprocessing
num_cols = X.select_dtypes(include=['int64', 'float64']).columns
cat_cols = X.select_dtypes(include=['object']).columns

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_cols)
    ])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Models
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
    'XGBoost': xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42),
    'LightGBM': lgb.LGBMRegressor(n_estimators=100, learning_rate=0.05, num_leaves=31, random_state=42, verbosity=-1)
}

results = {}

for name, model in models.items():
    pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', model)])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    results[name] = r2_score(y_test, y_pred)

# Add Ensemble
ensemble = VotingRegressor(estimators=[
    ('rf', models['Random Forest']),
    ('xgb', models['XGBoost']),
    ('lgb', models['LightGBM']),
    ('ridge', Ridge(alpha=1.0))
])
pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('model', ensemble)])
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
results['Voting Ensemble'] = r2_score(y_test, y_pred)

# Plotting
plt.figure(figsize=(12, 7))
sns.set_style("whitegrid")

# Sort results
sorted_results = dict(sorted(results.items(), key=lambda item: item[1]))

names = list(sorted_results.keys())
scores = [score * 100 for score in sorted_results.values()] # Convert to percentage

colors = ['#ff9999' if name == 'Linear Regression' else '#66b3ff' for name in names]
colors[-1] = '#99ff99' # Highlight the ensemble

bars = plt.barh(names, scores, color=colors, edgecolor='black', linewidth=1.5)

plt.xlabel('R² Accuracy (%)', fontsize=14, fontweight='bold')
plt.title('Model Accuracy Comparison (Test Data)', fontsize=16, fontweight='bold', pad=20)
plt.xlim(0, max(scores) + 10)

# Add value labels
for bar in bars:
    width = bar.get_width()
    plt.text(width + 1, bar.get_y() + bar.get_height()/2.,
             f'{width:.1f}%',
             ha='left', va='center', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('stress_comparison_beautiful.png', dpi=300)
print("Saved stress_comparison_beautiful.png")
