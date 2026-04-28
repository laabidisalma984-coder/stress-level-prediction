import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('🎓 Stress Prediction Model - Beautiful Overview', 
             fontsize=18, fontweight='bold', y=0.995)

# 1. Model Performance Comparison
models = ['Linear\nRegression', 'Random\nForest', 'Gradient\nBoosting']
r2_scores = [0.5109, 0.3875, 0.3739]
mae_scores = [1.4216, 1.5899, 1.6531]
colors_perf = ['#2ecc71', '#95a5a6', '#95a5a6']

ax = axes[0, 0]
x_pos = np.arange(len(models))
width = 0.35

bars1 = ax.bar(x_pos - width/2, r2_scores, width, label='R² Score', 
               color=colors_perf, edgecolor='black', linewidth=2, alpha=0.8)
ax2 = ax.twinx()
bars2 = ax2.bar(x_pos + width/2, mae_scores, width, label='MAE', 
                color=['#3498db', '#e74c3c', '#e74c3c'], edgecolor='black', linewidth=2, alpha=0.8)

ax.set_ylabel('R² Score', fontsize=12, fontweight='bold')
ax2.set_ylabel('Mean Absolute Error', fontsize=12, fontweight='bold')
ax.set_title('📊 Model Performance Comparison', fontsize=13, fontweight='bold', pad=10)
ax.set_xticks(x_pos)
ax.set_xticklabels(models, fontsize=11)
ax.set_ylim([0, 0.6])
ax2.set_ylim([0, 2])

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
           f'{height:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

# Add legend
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend([bars1, bars2], ['R² Score', 'MAE'], loc='upper right', fontsize=10)

# 2. Stress Prediction Examples
ax = axes[0, 1]
examples = ['Low Stress\nStudent', 'Average\nStudent', 'High Stress\nStudent']
predictions = [2.62, 6.52, 9.98]
colors_stress = ['#2ecc71', '#f39c12', '#e74c3c']
descriptions = ['✅ Well-rested,\nlow workload', '⚠️ Moderate\nfactors', '🚨 Sleep-deprived,\nhigh workload']

bars = ax.barh(examples, predictions, color=colors_stress, edgecolor='black', linewidth=2.5, height=0.6)
ax.set_xlabel('Predicted Stress Level (1-10)', fontsize=12, fontweight='bold')
ax.set_title('🎯 Example Predictions', fontsize=13, fontweight='bold', pad=10)
ax.set_xlim([0, 10.5])
ax.axvline(x=5, color='gray', linestyle='--', linewidth=1.5, alpha=0.5, label='Average')

# Add stress level zones
ax.axvspan(0, 3, alpha=0.1, color='green', label='Low')
ax.axvspan(3, 7, alpha=0.1, color='yellow', label='Moderate')
ax.axvspan(7, 10, alpha=0.1, color='red', label='High')

for i, (bar, pred, desc) in enumerate(zip(bars, predictions, descriptions)):
    ax.text(pred + 0.4, bar.get_y() + bar.get_height()/2, 
           f'{pred:.2f}/10\n{desc}', va='center', fontweight='bold', fontsize=9)

ax.set_yticks(range(len(examples)))
ax.set_yticklabels(examples, fontsize=11)

# 3. Top Stress Factors
ax = axes[1, 0]
factors = ['Academic\nWorkload', 'Major/\nField', 'Sleep\nHours', 'Upcoming\nExams', 'Age']
importance = [35.9, 11.5, 11.4, 9.0, 7.9]
colors_factors = ['#e74c3c', '#e67e22', '#f39c12', '#f1c40f', '#2ecc71']

bars = ax.bar(range(len(factors)), importance, color=colors_factors, 
              edgecolor='black', linewidth=2.5, alpha=0.85)
ax.set_ylabel('Importance Score (%)', fontsize=12, fontweight='bold')
ax.set_title('⭐ Top Stress Factors (Feature Importance)', fontsize=13, fontweight='bold', pad=10)
ax.set_xticks(range(len(factors)))
ax.set_xticklabels(factors, fontsize=11, fontweight='bold')
ax.set_ylim([0, 40])

# Add value labels on bars
for bar, imp in zip(bars, importance):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1, 
           f'{imp:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=11)

# Add a total line
ax.axhline(y=100/11, color='gray', linestyle='--', linewidth=1.5, alpha=0.5, 
          label=f'Equal weight ({100/11:.1f}%)')
ax.legend(fontsize=9)

# 4. Key Statistics & Insights
ax = axes[1, 1]
ax.axis('off')

stats_text = """
╔════════════════════════════════════════════╗
║     📊 MODEL & DATASET STATISTICS          ║
╠════════════════════════════════════════════╣
║                                            ║
║  Dataset Size:           545 Students      ║
║  Features Used:          11 Predictors     ║
║  Train/Test Split:       80% / 20%         ║
║  Train Samples:          436               ║
║  Test Samples:           109               ║
║                                            ║
║  Best Model:             Linear Regression ║
║  R² Score (Test):        0.5109 (51%)      ║
║  MAE (Mean Error):       ±1.42 points      ║
║  RMSE:                   1.77              ║
║  Cross-Validation R²:    0.4687 ± 0.0707  ║
║                                            ║
╠════════════════════════════════════════════╣
║            🎯 KEY INSIGHTS                 ║
╠════════════════════════════════════════════╣
║                                            ║
║  🔴 #1 STRESS FACTOR: Academic Workload    ║
║     (36% importance) - Most critical!      ║
║                                            ║
║  🟠 #2: Major/Field (11.5%)                ║
║     Different programs have different      ║
║     stress levels                          ║
║                                            ║
║  🟡 #3: Sleep Hours (11.4%)                ║
║     Sleep deprivation significantly        ║
║     impacts stress                         ║
║                                            ║
║  🟠 #4: Upcoming Exams (9%)                ║
║     Exams in next 2 weeks increase stress  ║
║                                            ║
║  🟢 #5: Age (7.9%)                         ║
║     Minor but measurable effect            ║
║                                            ║
╠════════════════════════════════════════════╣
║           💡 RECOMMENDATIONS               ║
╠════════════════════════════════════════════╣
║                                            ║
║  FOR LOW STRESS (<4/10):                   ║
║  ✅ Maintain current routines              ║
║  ✅ 7-8 hours sleep per night              ║
║  ✅ Continue physical activity             ║
║                                            ║
║  FOR MODERATE STRESS (4-7/10):             ║
║  ⚠️  Monitor workload closely              ║
║  ⚠️  Add exercise (30 min/day)             ║
║  ⚠️  Improve sleep quality                 ║
║                                            ║
║  FOR HIGH STRESS (>7/10):                  ║
║  🚨 Seek academic/counseling support       ║
║  🚨 Prioritize sleep (7-8+ hours)          ║
║  🚨 Reduce caffeine intake                 ║
║  🚨 Build support network                  ║
║                                            ║
╚════════════════════════════════════════════╝
"""

ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
       fontsize=9.5, verticalalignment='top', fontfamily='monospace',
       bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3, 
                pad=1, edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('stress_comparison_beautiful.png', dpi=300, bbox_inches='tight', 
           facecolor='white', edgecolor='black')
print("✅ Beautiful comparison dashboard saved as: stress_comparison_beautiful.png")
# plt.show() removed - image already saved
