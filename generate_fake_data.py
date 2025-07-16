from faker import Faker
import random
import uuid

from sqlalchemy.orm import Session
from database import SessionLocal
from models import Patient

fake = Faker()

def calculate_bmi(weight: float, height: float) -> float:
    return round(weight / (height ** 2), 2)

def calculate_verdict(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def generate_fake_patient() -> dict:
    gender = random.choice(['male', 'female', 'Others'])
    height = round(random.uniform(1.4, 2.0), 2)  # in meters
    weight = round(random.uniform(40, 120), 1)   # in kg
    bmi = calculate_bmi(weight, height)
    verdict = calculate_verdict(bmi)

    return {
        "id": f"P{str(uuid.uuid4())[:8]}",  # Unique ID like P7c6f2d1a
        "name": fake.name(),
        "city": fake.city(),
        "age": random.randint(1, 99),
        "gender": gender,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "verdict": verdict
    }

def insert_fake_patients(count: int = 100):
    db: Session = SessionLocal()
    for _ in range(count):
        patient_data = generate_fake_patient()
        patient = Patient(**patient_data)
        db.add(patient)
    try:
        db.commit()
        print(f"Inserted {count} fake patients into the database.")
    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    insert_fake_patients(100)
