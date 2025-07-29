from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse 
import json
from pydantic import BaseModel,computed_field,Field
from typing import Literal,Annotated

app = FastAPI() # making object

class Patient(BaseModel):
    
    id : Annotated[str,Field(max_length=30,title='Enter patients Id: ',examples=['P001'])]
    name: Annotated[str,Field(max_length=30,title='Enter patients name: ',examples=['Raj shukla','pappu bhai'])]
    city: Annotated[str,Field(max_length=30,title='Enter patients city: ',examples=['Ahmedabad'])]
    height:Annotated[float,Field(gt=0,title='Enter patients height in meters: ',examples=['1.72','1.43'])]
    weight:Annotated[float,Field(gt=0,title='Enter patients weight in kgs: ',examples=['1.72','1.43'])]
    gender:Annotated[Literal['male','female'],Field(...,title='Enter gender of the patient: ')]
    
    @computed_field
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    
    @computed_field
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 35:
            return 'Normal'
        else:
            return 'Overweight'
        



def save_data(data):
    with open('PatientData.json','w') as f:
        json.dump(data,f)
        
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
        raise HTTPException(status_code=400,detail='Bad request')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Bad request')

    order_by = True if order == 'desc' else False
    
    sorted_data = sorted(data.values(),key = lambda x: x.get(sort_by,0), reverse = order_by)
    
    return sorted_data

@app.post('/create')
def Add_patient(patient: Patient):
    
    # load data
    data = load_json()
    
    # check if the patient already exiest
    if patient.id in data:
        raise HTTPException(status_code = 400,detail = 'Patient already exiest')
    
    # Add Patient
    data[patient.id] = patient.model_dump(exclude=['id'])
    
    #save model
    save_data(data)
    
    return JSONResponse(status_code = 201,content = {'New Patient created successfully'})
    