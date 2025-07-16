from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
import models
from typing import Literal
from models import Patient
from schemas import PatientUpdate,PatientInput
from fastapi.responses import JSONResponse
from fastapi import Request
from model import predict_verdict


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
    return {"message": "API to manage patient records using PostgreSQL"}

@app.get("/view", response_model=list[schemas.PatientOut])
def view_all(db: Session = Depends(get_db)):
    return crud.get_all_patients(db)

@app.get("/patient/{patient_id}", response_model=schemas.PatientOut)
def view_patient(patient_id: str = Path(...), db: Session = Depends(get_db)):
    patient = crud.get_patient(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@app.get("/sort")
def sort_patients(
    sort_by: Literal["height", "weight", "bmi"] = Query(..., description="Field to sort by"),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order"),
    db: Session = Depends(get_db)
):
    return crud.sort_patients(db, sort_by, order)

@app.post('/create', response_model=schemas.PatientOut)
def create(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    # 1. Fetch the patient from DB
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # 2. Extract updates
    updates = patient_update.model_dump(exclude_unset=True)

    # 3. Apply changes
    for field, value in updates.items():
        setattr(patient, field, value)

    # 4. If height or weight updated, recalculate bmi and verdict
    if 'height' in updates or 'weight' in updates:
        patient.bmi = round(patient.weight / (patient.height ** 2), 2)
        if patient.bmi < 18.5:
            patient.verdict = "Underweight"
        elif patient.bmi < 25:
            patient.verdict = "Normal"
        elif patient.bmi < 30:
            patient.verdict = "Overweight"
        else:
            patient.verdict = "Obese"

    # 5. Commit the update
    db.commit()
    db.refresh(patient)

    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})

@app.middleware("http")
async def log_request(request: Request, call_next):
    body = await request.body()
    print(f"Request body: {body.decode()}")
    response = await call_next(request)
    return response

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    
    return {"message": f"Patient with id {patient_id} deleted successfully"}

@app.post("/predict/")
def get_prediction(data: PatientInput):
    try:
        result = predict_verdict(data.age, data.bmi, data.gender)
        return {"verdict": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))