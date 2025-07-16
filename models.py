from sqlalchemy import Column, String, Integer, Float
from database import Base

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    city = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    bmi = Column(Float)
    verdict = Column(String)