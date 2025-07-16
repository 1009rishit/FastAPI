from pydantic import BaseModel, Field, computed_field
from typing import Literal, Optional, Annotated

class PatientBase(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', example='P001')]
    name: Annotated[str, Field(...,description='Name of the project')]
    city: Annotated[str, Field(...,description='City where the patient is living')]
    age: Annotated[int, Field(...,gt=0,lt=100,description='Age of the patient')]
    gender: Annotated[Literal['male','female','Others'],Field(...,description='Gender of the patient')]
    height: Annotated[float, Field(...,gt=0,description='Height of the patient')]
    weight: Annotated[float, Field(...,gt=0,description='Weight of the patient')]
    

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientCreate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None,gt=0)]
    gender: Annotated[Optional[Literal['male','female','Others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None,gt=0)]
    weight: Annotated[Optional[float], Field(default=None,gt=0)]

class PatientOut(PatientCreate):
    bmi: float
    verdict: str

    class Config:
        from_attributes = True

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal['male', 'female', 'Others']] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

class PatientInput(BaseModel):
    age: int = Field(...,gt=0,example=30)
    bmi: float = Field(..., example=24.5)
    gender: str = Field(..., example="male")