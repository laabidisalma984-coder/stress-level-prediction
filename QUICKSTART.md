# 🚀 Quick Start Guide - Stress Prediction Model

## Installation

All required packages are already installed. To verify:

```bash
pip list | findstr "pandas numpy scikit-learn matplotlib seaborn"
```

## Running the Model

### 1. Train the Model & Generate Analysis
```bash
python stress_prediction_model.py
```

**Output:**
- Model performance metrics
- Feature importance rankings
- Visualizations (stress_prediction_analysis.png)

### 2. Make Predictions on New Students
```bash
python stress_prediction_interface.py
```

**Output:**
- Example predictions for 3 students
- Demonstrates how to use the prediction system

## Making Custom Predictions

### Python Code Template

```python
from stress_prediction_interface import predict_stress_level

# Customize these values for your student
result = predict_stress_level(
    age=21,                              # Integer: student's age
    degree='licence',                    # See list below
    year_of_study='2nd',                 # '1st', '2nd', '3rd', '4th', '5th'
    major='Psychology',                  # See list below
    sleep_hours_category='7–8 hours',    # See options below
    screen_time_category='2–4 hours',    # See options below
    physical_activity='yes',             # 'yes' or 'no'
    caffeine_drinks_category='1',        # '0', '1', '2', '3 or more'
    study_hours_category='10–20 hours',  # See options below
    exam_soon='no',                      # 'yes' or 'no'
    workload_level='low'                 # 'low', 'moderate', 'high'
)

# Print results
print(f"Stress Level: {result['predicted_stress_level']}/10")
print(f"Category: {result['stress_category']}")
print(f"Confidence: {result['confidence']}")
```

## Valid Input Values

### Degree Types
```
'cycle d'ingénieur'
'licence'
'mastère'
'préparatoire intégrée'
'doctorat'
'médecine'
'pharmacie'
'Bachelor degree at TBS'  (or similar)
```

### Year of Study
```
'1st', '2nd', '3rd', '4th', '5th'
```

### Sleep Hours Category
```
'Less than 5 hours'
'5–6 hours'
'7–8 hours'
'More than 8 hours'
```

### Screen Time Category
```
'Less than 2 hours'
'2–4 hours'
'4–6 hours'
'More than 6 hours'
```

### Study Hours Category
```
'Less than 10 hours'
'10–20 hours'
'20–30 hours'
'More than 30 hours'
```

### Common Majors (50+ available)
```
'IT'
'AI'
'Computer Science'
'Healthcare IT'
'Biomedical Engineering'
'Mechanical Engineering'
'Telecommunications Engineering'
'Network Security'
'Psychology'
'Law'
'Medicine'
'Pharmacie'
'Business Administration'
'Economics'
'English'
'Architecture and Urban Planning'
... and many more
```

## Understanding Results

### Stress Level Scale
- **1-3**: Low Stress - Student doing well
- **4-6**: Moderate Stress - Some challenges but manageable
- **7-10**: High Stress - Needs intervention/support

### Interpretation

```
Predicted Stress Level: 2.62/10 (Low)
→ Student is doing well, maintain current strategies

Predicted Stress Level: 5.50/10 (Moderate)
→ Student needs some support, monitor closely

Predicted Stress Level: 8.75/10 (High)
→ Student needs immediate support/intervention
```

## Key Insights from Model

### Top Factors Affecting Stress (in order)
1. **Academic Workload** (36%) - Most important!
2. **Major/Field** (11.5%) - Varies by program
3. **Sleep Hours** (11.4%) - Critical factor
4. **Upcoming Exams** (9%) - Significant impact
5. **Age** (8%) - Some age-related variation

### Recommendations by Stress Level

**Low Stress (< 4/10)**
✅ Keep doing what you're doing!
✅ Get 7-8 hours of sleep
✅ Limit screen time
✅ Exercise regularly

**Moderate Stress (4-7/10)**
⚠️ Monitor workload
⚠️ Increase sleep to 7-8 hours if possible
⚠️ Add physical activity (30 min/day)
⚠️ Consider study groups

**High Stress (> 7/10)**
🆘 Talk to academic advisor
🆘 Seek counseling support
🆘 Prioritize sleep (7-8+ hours)
🆘 Reduce caffeine intake
🆘 Increase physical activity
🆘 Build support network

## Model Accuracy

- **R² Score**: 0.51 (explains 51% of stress variation)
- **Average Error**: ±1.42 points on 10-point scale
- **Reliability**: Good for identifying high vs. low stress

## Troubleshooting

### Error: "Unknown degree"
**Solution**: Copy the exact degree name from the dataset
```python
# Examples that work:
'cycle d'ingénieur'  # Not "engineering cycle"
'licence'            # Not "bachelor"
'mastère'            # Not "master"
```

### Error: "Unknown major"
**Solution**: Check the major name in the dataset
- Use exact spelling and capitalization
- Common issue: extra spaces (e.g., "IT " vs "IT")

### Error: "Unknown sleep/screen/study category"
**Solution**: Use exact category names including punctuation
```python
'5–6 hours'           # Note the en-dash (–) not hyphen (-)
'More than 8 hours'   # Exact capitalization
```

## Files Reference

| File | Purpose |
|------|---------|
| `stress_prediction_model.py` | Train model, evaluate performance |
| `stress_prediction_interface.py` | Make predictions for new students |
| `dataset_ml_500.csv` | Original survey data (545 students) |
| `README.md` | Detailed documentation |
| `QUICKSTART.md` | This file |
| `stress_prediction_analysis.png` | Visualizations and model metrics |

## Next Steps

1. ✅ Train model: `python stress_prediction_model.py`
2. ✅ Test predictions: `python stress_prediction_interface.py`
3. ✅ Modify examples in `stress_prediction_interface.py`
4. ✅ Create custom analysis or web interface

## Support & Questions

Refer to the `README.md` for:
- Detailed model documentation
- Technical specifications
- Limitations and future improvements
- Statistical analysis details

---

**Happy stress prediction! 📊**
