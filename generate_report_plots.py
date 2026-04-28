import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import joblib

print("Generating Confusion Matrix...")

# Load dataset
df = pd.read_csv('dataset_ml_extended.csv')
X = df.iloc[:, 1:-1]
y = df.iloc[:, -1].astype(int)

# Split (must match the training split to evaluate on test data)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load model
pipeline = joblib.load('stress_model_v2.joblib')

# Predict and round to nearest integer to simulate classification
y_pred_continuous = pipeline.predict(X_test)
y_pred_rounded = np.clip(np.round(y_pred_continuous), 1, 10).astype(int)

# Generate Confusion Matrix
labels = range(1, 11)
cm = confusion_matrix(y_test, y_pred_rounded, labels=labels)

# Plotting
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=labels, yticklabels=labels)

plt.xlabel('Predicted Stress Level', fontsize=12, fontweight='bold')
plt.ylabel('Actual Stress Level', fontsize=12, fontweight='bold')
plt.title('Confusion Matrix (Rounded Predictions)', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=300)

print("Saved confusion_matrix.png")
