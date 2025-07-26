from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI() # making object

def load_json():
    with open('PatientData.json','r') as f:
        data = json.load(f)
    return data

@app.get('/') #  creating route using '/' decorater
def hello():
    return {'message':'Patient Data Handing API'} # returns dictionary

@app.get('/about')
def Me():
    return {'Description':'This is the API created for managing Patient Records'}

@app.get('/view')
def get_data():
    data = load_json()
    return data

@app.get('/patient/{patient_id}')
def get_id(patient_id: str = Path(...,description='Patiant ID')):
    data = load_json()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail = 'Patient not found')

@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = 'Sort the values by height,weight or bmi'),order:str = Query('asc',description='Eneetr the asc or desc')):
    
    valied_fields = ['height', 'weight', 'bmi']
    data = load_json()
    
    if sort_by not in valied_fields:
        return HTTPException(status_code=400,detail='Bad request')

    if order not in ['asc','desc']:
        return HTTPException(status_code=400,detail='Bad request')

    order_by = True if order == 'desc' else False
    
    sorted_data = sorted(data.values(),key = lambda x: x.get(sort_by,0), reverse = order_by)
    
    return sorted_data

