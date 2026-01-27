import pandas as pd

# 1. Load the CSV file
# Replace 'medical_data.csv' with your actual filename
df = pd.read_csv('disease_diagnosis.csv')

# 2. Split Blood Pressure into two separate numerical columns
# This turns "120/80" into two columns: 120 and 80
df[['Systolic', 'Diastolic']] = df['Blood_Pressure_mmHg'].str.split('/', expand=True).astype(int)

# 3. Create a 'Fever' flag (Body Temp > 38.0 C is generally a fever)
df['Has_Fever'] = df['Body_Temperature_C'] > 38.0

# 4. Reorganize columns for better flow
cols = ['Patient_ID', 'Age', 'Gender', 'Diagnosis', 'Severity', 
        'Heart_Rate_bpm', 'Body_Temperature_C', 'Systolic', 'Diastolic', 'Oxygen_Saturation_%']
df_organized = df[cols]

# 5. Display the first 10 rows in a clean format
print(df_organized.head(2000).to_string(index=False))