# Stress Level Prediction Model for University Students

## 📋 Project Overview

This project builds a machine learning model to predict stress levels of university students based on their lifestyle, academic, and personal characteristics. The model analyzes 545 student survey responses to identify key stress factors and make personalized predictions.

## 📊 Dataset Information

- **Total Samples**: 545 students
- **Survey Period**: February 26 - April 2, 2026
- **Features**: 11 key predictors
- **Target**: Stress level (1-10 scale)

### Features Used

1. **Age** - Student age (encoded)
2. **Degree Type** - Programme (licence, engineering cycle, master, doctorate, medicine, pharmacy)
3. **Year of Study** - Academic year (1st, 2nd, 3rd, 4th, 5th)
4. **Major/Field** - Area of study (50+ different majors)
5. **Sleep Hours** - Average sleep per night (mapped from categories)
6. **Screen Time** - Daily screen time excluding academic work (mapped from categories)
7. **Physical Activity** - Regular exercise (yes/no)
8. **Caffeine Consumption** - Daily caffeinated drinks (0-3+)
9. **Study Hours** - Weekly study hours outside class (mapped from categories)
10. **Exam Status** - Exams in next 2 weeks (yes/no)
11. **Academic Workload** - Self-rated workload (low/moderate/high)

## 🎯 Key Findings

### Top Stress Factors (by importance)
1. **Academic Workload** (35.9%) - Most influential factor
2. **Major/Field** (11.5%) - Different majors have varying stress levels
3. **Sleep Hours** (11.4%) - Sleep deprivation significantly impacts stress
4. **Exams in 2 weeks** (9.0%) - Upcoming exams increase stress
5. **Age** (7.9%) - Age-related differences in stress

### Stress Level Statistics
- **Minimum**: 1 (very low)
- **Maximum**: 10 (very high)
- **Average**: 5.89
- **Standard Deviation**: 2.65

## 🤖 Model Performance

### Best Model: **Linear Regression**

| Metric | Value |
|--------|-------|
| Test R² Score | 0.5109 |
| Test MAE | 1.42 |
| Test RMSE | 1.77 |
| Cross-Validation R² | 0.4687 ± 0.0707 |

**Interpretation**: 
- The model explains ~51% of stress level variance
- Average prediction error is ±1.42 points on the 10-point scale
- Reliable for identifying high vs. low stress students

### Other Models Tested

| Model | Test R² | Test MAE | Status |
|-------|---------|----------|--------|
| Random Forest | 0.3875 | 1.59 | Overfitting |
| Gradient Boosting | 0.3739 | 1.65 | Overfitting |

Linear Regression was selected as the best model due to better generalization despite lower training performance.

## 📈 Example Predictions

### Example 1: Low-Stress Student
```
Profile:
- Well-rested (7-8 hours sleep)
- Low screen time (2-4 hours)
- Regular physical activity
- Moderate caffeine (1 drink/day)
- Moderate study hours
- No upcoming exams
- Low workload

Predicted Stress Level: 2.62/10 (Low)
```

### Example 2: High-Stress Student
```
Profile:
- Sleep-deprived (< 5 hours)
- Heavy screen time (> 6 hours)
- No physical activity
- High caffeine (3+ drinks/day)
- Heavy study hours (20-30/week)
- Exams in next 2 weeks
- High workload

Predicted Stress Level: 9.98/10 (High)
```

### Example 3: Average Student
```
Profile:
- Moderate sleep (5-6 hours)
- Moderate screen time (4-6 hours)
- Regular physical activity
- Low-moderate caffeine (1 drink/day)
- Moderate study hours (10-20/week)
- Exams in next 2 weeks
- Moderate workload

Predicted Stress Level: 6.52/10 (Moderate)
```

## 🛠️ Files in Project

1. **stress_prediction_model.py**
   - Main model training script
   - Data preprocessing and exploration
   - Model comparison and evaluation
   - Feature importance analysis
   - Visualization generation

2. **stress_prediction_interface.py**
   - Prediction interface for new students
   - Pre-trained model predictions
   - Example predictions for demonstration

3. **stress_prediction_analysis.png**
   - Feature importance chart
   - Model comparison
   - Predictions vs. actual scatter plot
   - Residuals analysis

4. **dataset_ml_500.csv**
   - Original survey data
   - 545 responses with 13 columns

5. **README.md** (this file)
   - Project documentation
   - Model details and results

## 🚀 Usage Instructions

### Running the Model

```bash
# Train the model and generate analysis
python stress_prediction_model.py

# Make predictions on new students
python stress_prediction_interface.py
```

### Making Predictions on New Students

```python
from stress_prediction_interface import predict_stress_level

# Predict stress for a student
result = predict_stress_level(
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

print(f"Predicted Stress: {result['predicted_stress_level']}/10")
print(f"Category: {result['stress_category']}")
```

### Parameter Options

**sleep_hours_category**: 'Less than 5 hours', '5–6 hours', '7–8 hours', 'More than 8 hours'

**screen_time_category**: 'Less than 2 hours', '2–4 hours', '4–6 hours', 'More than 6 hours'

**physical_activity**: 'yes' or 'no'

**caffeine_drinks_category**: '0', '1', '2', '3 or more'

**study_hours_category**: 'Less than 10 hours', '10–20 hours', '20–30 hours', 'More than 30 hours'

**exam_soon**: 'yes' or 'no'

**workload_level**: 'low', 'moderate', 'high'

## 💡 Recommendations Based on Model Insights

### For High-Stress Students (>7/10)
1. **Improve sleep**: Aim for 7-8 hours minimum
2. **Reduce screen time**: Limit to 2-4 hours outside of academics
3. **Add physical activity**: Regular exercise reduces stress
4. **Manage caffeine**: Limit to 1-2 drinks per day
5. **Seek academic support**: Talk to professors about workload

### For Moderate-Stress Students (4-7/10)
1. **Maintain balance**: Continue current routines that work
2. **Watch for red flags**: Monitor exam periods closely
3. **Preventive measures**: Establish good sleep and exercise habits
4. **Workload monitoring**: Communicate with academic advisors if workload increases

### For Low-Stress Students (<4/10)
1. **Maintain routines**: Continue successful strategies
2. **Help others**: Consider peer support roles
3. **Gradual challenges**: Take on new opportunities without overload

## 📚 Technical Details

### Data Preprocessing Steps
1. Removed timestamp column
2. Mapped categorical variables to numerical values
3. Encoded student characteristics (age, degree, year, major)
4. Handled categorical ranges (sleep, screen time, study hours)
5. Feature scaling using StandardScaler (zero mean, unit variance)
6. Train-test split: 80% training, 20% testing

### Model Training
- Algorithm: Linear Regression
- Train samples: 436
- Test samples: 109
- Cross-validation: 5-fold

### Performance Metrics
- **R² Score**: Proportion of variance explained
- **MAE (Mean Absolute Error)**: Average prediction error in points
- **RMSE (Root Mean Square Error)**: Penalizes larger errors

## 📋 Requirements

```
pandas>=1.0
numpy>=1.18
scikit-learn>=0.24
matplotlib>=3.3
seaborn>=0.11
```

## ⚠️ Limitations

1. **Model scope**: Specific to surveyed student population
2. **Cross-cultural generalization**: May not apply to all universities/countries
3. **Temporal dynamics**: Model trained on Feb-Apr 2026 data; stress patterns may vary seasonally
4. **Self-reported data**: Responses subject to recall bias
5. **51% variance explained**: Implies 49% of stress variation from unmeasured factors (e.g., personal relationships, family issues, mental health conditions)

## 🔮 Future Improvements

1. **Collect more data**: Increase sample size for better generalization
2. **Add temporal features**: Track stress changes over time
3. **Include qualitative data**: Analyze written responses for deeper insights
4. **Non-linear models**: Test neural networks for complex patterns
5. **Real-time monitoring**: Build web/mobile app for ongoing stress tracking
6. **Intervention tracking**: Measure effectiveness of stress reduction strategies
7. **Demographic analysis**: Separate models for different student subgroups

## 📞 Contact & Support

For questions or improvements to this model, please refer to the project documentation and code comments.

---

**Model Created**: April 25, 2026
**Dataset Size**: 545 students
**Best Model**: Linear Regression (R² = 0.5109)
