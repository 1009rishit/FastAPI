import json
from database import SessionLocal
from schemas import PatientCreate
import crud

with open('data.json') as f:
    data = json.load(f)

db = SessionLocal()

for patient_id, details in data.items():
    try:
        patient = PatientCreate(id=patient_id, **details)
        crud.create_patient(db, patient)
    except Exception as e:
        print(f"Error migrating patient {patient_id}: {e}")
