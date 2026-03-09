from fastapi import FastAPI, HTTPException
from fastapi import Path, Query
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
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_pateints(sort_by: str = Query(..., description="Sort on the basis of height, weight, or BMI"), 
                  order: str = Query('asc', description="Sort order: 'asc' for ascending, 'desc' for descending")):

    valid_fields = ['height', 'weight', 'BMI']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of: {valid_fields}")

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'")
    
    data = load_data()
    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse= sort_order)
    return sorted_data

