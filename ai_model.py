import pandas as pd
import io
import sys
from datetime import datetime

# Path setup (Keeping your original logic)
path = '/home/yourusername/'
if path not in sys.path:
    sys.path.append(path)

# Try importing your AI model if needed, though we'll use the CSV logic below
# from ai_model import ai_model as application 

def generate_report(symptoms, hr, temp, bp, predictions):
    """Creates the text content for the medical report."""
    report = f"MEDICAL REPORT\nDate: {datetime.now()}\n"
    report = f"{'='*30}\n"
    report += f"Vitals: HR {hr} bpm, Temp {temp}C, BP {bp}\n"
    report += f"Symptoms: {symptoms}\n\n"
    report += "Predictions:\n"
    for diag, prob in predictions.items():
        report += f"- {diag}: {prob*100:.1f}%\n"
    return report

def main():
    # Load data
    try:
        df = pd.read_csv('disease_diagnosis.csv')
    except FileNotFoundError:
        print("Error: 'disease_diagnosis.csv' not found.")
        return

    print("--- Disease Diagnosis System ---")
    
    # Get user inputs (Replacing Flask request.form)
    symptoms_raw = input("Enter symptoms separated by commas: ")
    hr = input("Enter Heart Rate (bpm): ")
    temp = input("Enter Temperature (C): ")
    bp = input("Enter Blood Pressure: ")

    # Process input_list
    input_list = [s.strip().capitalize() for s in symptoms_raw.split(',')]
    
    # Logic to find diagnosis
    condition = df[['Symptom_1', 'Symptom_2', 'Symptom_3']].isin(input_list).any(axis=1)
    matches = df[condition]

    if not matches.empty:
        # Calculate predictions
        prediction = matches['Diagnosis'].value_counts(normalize=True).head(3).to_dict()
        
        # Display results to console
        print("\nTop Predictions:")
        for diag, prob in prediction.items():
            print(f"- {diag}: {prob*100:.1f}%")

        # Create report
        report_data = generate_report(symptoms_raw, hr, temp, bp, prediction)
        
        # Save to file (Replacing Flask send_file)
        save_choice = input("\nWould you like to save this report to a file? (y/n): ").lower()
        if save_choice == 'y':
            filename = f"Medical_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
            with open(filename, 'w') as f:
                f.write(report_data)
            print(f"Report saved successfully as {filename}")
    else:
        print("\nNo matching diagnosis found based on provided symptoms.")

if __name__ == '__main__':
    main()