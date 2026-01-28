import sys
path = '/home/yourusername/'
if path not in sys.path:
    sys.path.append(path)

from ai_model import ai_model as application  # This must match your 'app.py' filename

import pandas as pd
import io
from datetime import datetime

app = Flask(__name__)

# Load data
df = pd.read_csv('disease_diagnosis.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    report_data = ""
    
    if request.method == 'POST':
        # Get data from form
        symptoms_raw = request.form.get('symptoms')
        hr = request.form.get('hr')
        temp = request.form.get('temp')
        bp = request.form.get('bp')

        # Logic to find diagnosis
        input_list = [s.strip().capitalize() for s in symptoms_raw.split(',')]
        condition = df[['Symptom_1', 'Symptom_2', 'Symptom_3']].isin(input_list).any(axis=1)
        matches = df[condition]

        if not matches.empty:
            prediction = matches['Diagnosis'].value_counts(normalize=True).head(3).to_dict()
            
            # Create the report content for the download
            report_data = f"MEDICAL REPORT\nDate: {datetime.now()}\n"
            report_data += f"Vitals: HR {hr} bpm, Temp {temp}C, BP {bp}\n"
            report_data += f"Symptoms: {symptoms_raw}\n\nPredictions:\n"
            for diag, prob in prediction.items():
                report_data += f"- {diag}: {prob*100:.1f}%\n"

    return render_template('index.html', prediction=prediction, report_data=report_data)

@app.route('/download', methods=['POST'])
def download():
    # Receive the report text and turn it into a downloadable file
    report_text = request.form.get('report_text')
    buffer = io.BytesIO()
    buffer.write(report_text.encode())
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"Medical_Report_{datetime.now().strftime('%Y%m%d')}.txt",
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True)