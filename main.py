from fastapi import FastAPI
from fastapi import Path
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    
    return data 

#define the route for our requests (get request)
@app.get('/')
def hello():
    return {'message': 'Patients Management System API'}

@app.get('/about')
def about():
    return {'message':'A fully functional API to manage patients records'}

@app.get('/view')
def view_patients():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    return {'message': 'Patient not found'}
