from fastapi import FastAPI
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