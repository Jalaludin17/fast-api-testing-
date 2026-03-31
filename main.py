from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional, Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id : Annotated[str, Field(..., description="Unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(..., description="Full name of the patient", example="John Doe")]
    city : Annotated[str, Field(..., description="City of residence", example="New York")]
    age : Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient", example=30)]
    gender : Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender of the patient", example="Male")]
    height : Annotated[float, Field(..., gt=0, description="Height of the patient in meters", example=1.75)]
    weight : Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms", example=70.5)]

@computed_field
@property
def bmi(self) -> float:
    bmi=round(self.weight / (self.height ** 2), 2)
    return bmi

@computed_field
@property
def verdict(self) -> str:
    if self.bmi < 18.5:
        return "underweight"
    elif self.bmi < 25:
        return "normal weight"
    elif self.bmi < 30:
        return "overweight"
    else:
        return "obese"

#update endpoint
class PatientUpdate(BaseModel):
    name: Optional[Annotated[str, Field(None, description="Full name of the patient", example="John Doe")]]
    city : Optional[Annotated[str, Field(None, description="City of residence", example="New York")]]
    age : Optional[Annotated[int, Field(None, gt=0, lt=120, description="Age of the patient", example=30)]]
    gender : Optional[Annotated[Literal["Male", "Female", "Other"], Field(None, description="Gender of the patient", example="Male")]]
    height : Optional[Annotated[float, Field(None, gt=0, description="Height of the patient in meters", example=1.75)]]
    weight : Optional[Annotated[float, Field(None, gt=0, description="Weight of the patient in kilograms", example=70.5)]]          

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    
    return data 

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

#Retrieve 
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

#Create 
@app .post('/create')
def create_patient(patient: Patient):
    data = load_data() #it will bring all over data from json file and store in data variable as a dictionary
    
    #check patient existance 
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    
    #add new patient to data (merging old and new data)
    data[patient.id] = patient.model_dump(exclude={'id'}) #it will convert the patient object into a dictionary and store it in data variable with key as patient.id
    
    #save the updated data back to the json file
    save_data(data) #it will save the updated data back to the json file
    
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

