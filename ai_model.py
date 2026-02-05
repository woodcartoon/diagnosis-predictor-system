import pandas as pd
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your HTML file to talk to this script
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data once when starting
df = pd.read_csv('disease_diagnosis.csv')

class DiagnosisRequest(BaseModel):
    symptoms: str
    hr: str
    temp: str
    bp: str

@app.post("/diagnose")
async def diagnose(data: DiagnosisRequest):
    # Process symptoms logic (Same as your original code)
    input_list = [s.strip().capitalize() for s in data.symptoms.split(',')]
    condition = df[['Symptom_1', 'Symptom_2', 'Symptom_3']].isin(input_list).any(axis=1)
    matches = df[condition]

    if not matches.empty:
        # Calculate top 3 predictions
        prediction = matches['Diagnosis'].value_counts(normalize=True).head(3).to_dict()
        
        # Format for the Frontend
        results = [{"name": k, "prob": f"{v*100:.1f}%"} for k, v in prediction.items()]
        return {"status": "success", "predictions": results}
    
    return {"status": "error", "message": "No diagnosis found"}