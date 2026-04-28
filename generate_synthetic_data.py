import pandas as pd
import numpy as np
import random
import datetime

print("Loading original dataset...")
df = pd.read_csv('dataset_ml_500.csv')
original_len = len(df)
print(f"Original dataset shape: {df.shape}")

N_SYNTHETIC = 2000

# Function to add noise to a row
def augment_row(row):
    new_row = row.copy()
    
    # 1. Add noise to Age (+/- 1 or 2 years)
    age = int(new_row["what's your age "])
    noise = random.choices([-2, -1, 0, 1, 2], weights=[0.05, 0.2, 0.5, 0.2, 0.05])[0]
    new_age = max(17, min(40, age + noise))
    new_row["what's your age "] = new_age
    
    # 2. Add noise to Stress Level (+/- 1)
    stress_col = "   On a scale from 1 to 10, how would you rate your current stress level?  "
    stress = int(new_row[stress_col])
    s_noise = random.choices([-1, 0, 1], weights=[0.15, 0.7, 0.15])[0]
    new_stress = max(1, min(10, stress + s_noise))
    new_row[stress_col] = new_stress
    
    # 3. Categorical variance (10% chance to slightly alter one category)
    if random.random() < 0.1:
        # Swap sleep category
        sleeps = ['Less than 5 hours', '5–6 hours', '7–8 hours', 'More than 8 hours']
        curr_sleep = new_row['  How many hours do you sleep on average per night?  ']
        if curr_sleep in sleeps:
            idx = sleeps.index(curr_sleep)
            shift = random.choice([-1, 1])
            new_idx = max(0, min(len(sleeps)-1, idx + shift))
            new_row['  How many hours do you sleep on average per night?  '] = sleeps[new_idx]
            
    # Modify timestamp slightly to make it unique
    try:
        dt = datetime.datetime.strptime(row['Timestamp'], "%d/%m/%Y %H:%M:%S")
        dt += datetime.timedelta(days=random.randint(1, 30), minutes=random.randint(1, 1440))
        new_row['Timestamp'] = dt.strftime("%d/%m/%Y %H:%M:%S")
    except:
        pass # Ignore if timestamp parsing fails
        
    return new_row

print(f"Generating {N_SYNTHETIC} synthetic rows...")
# Sample original dataset with replacement
synthetic_samples = df.sample(n=N_SYNTHETIC, replace=True, random_state=42)

# Apply augmentation
synthetic_df = synthetic_samples.apply(augment_row, axis=1)

# Combine datasets
combined_df = pd.concat([df, synthetic_df], ignore_index=True)

print(f"Combined dataset shape: {combined_df.shape}")
combined_df.to_csv('dataset_ml_extended.csv', index=False)
print("DONE: Saved new dataset to dataset_ml_extended.csv")
