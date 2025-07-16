from sqlalchemy.orm import Session
from models import Patient as DBPatient
from schemas import PatientCreate, PatientUpdate
from fastapi import HTTPException
from models import Patient
from sqlalchemy import asc, desc
import schemas,models


def calculate_verdict(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"
    


def get_all_patients(db: Session):
    return db.query(DBPatient).all()

def get_patient(db: Session, patient_id: str):
    patient = db.query(DBPatient).filter(DBPatient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

def sort_patients(db: Session, sort_by: str, order: str):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise ValueError(f"Invalid sort field. Choose from {valid_fields}")

    column = getattr(Patient, sort_by)
    direction = desc(column) if order == "desc" else asc(column)
    return db.query(Patient).order_by(direction).all()


def create_patient(db: Session, patient: schemas.PatientCreate):
    existing = db.query(models.Patient).filter(models.Patient.id == patient.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    bmi = round(patient.weight / (patient.height ** 2), 2)
    verdict = calculate_verdict(bmi)

    db_patient = models.Patient(
        id=patient.id,
        name=patient.name,
        city=patient.city,
        age=patient.age,
        gender=patient.gender,
        height=patient.height,
        weight=patient.weight,
        bmi=bmi,
        verdict=verdict
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def update_patient(db: Session, patient_id: str, updates: PatientUpdate):
    patient = get_patient(db, patient_id)
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(patient, key, value)
    db.commit()
    db.refresh(patient)
    return patient

def delete_patient(db: Session, patient_id: str):
    patient = get_patient(db, patient_id)
    db.delete(patient)
    db.commit()
