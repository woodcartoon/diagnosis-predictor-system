from flask import Flask, render_template, request
import pandas as pd
import difflib

app = Flask(__name__)

# Load and prepare data
df = pd.read_csv('disease_diagnosis.csv')
all_valid_symptoms = pd.unique(df[['Symptom_1', 'Symptom_2', 'Symptom_3']].values.ravel('K'))
all_valid_symptoms = [s for s in all_valid_symptoms if str(s) != 'nan']

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        # Get data from HTML form
        user_symptoms = request.form.get('symptoms').split(',')
        hr = request.form.get('hr')
        temp = request.form.get('temp')
        bp = request.form.get('bp')

        # Simple verification logic
        final_symptoms = [s.strip().capitalize() for s in user_symptoms if s.strip().capitalize() in all_valid_symptoms]
        
        if final_symptoms:
            condition = df[['Symptom_1', 'Symptom_2', 'Symptom_3']].isin(final_symptoms).any(axis=1)
            matches = df[condition]
            if not matches.empty:
                prediction = matches['Diagnosis'].value_counts(normalize=True).head(3).to_dict()

                # Save to TXT
                with open("web_report.txt", "w") as f:
                    f.write(f"Vitals: HR:{hr}, Temp:{temp}, BP:{bp}\nSymptoms: {final_symptoms}\nResults: {prediction}")

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)