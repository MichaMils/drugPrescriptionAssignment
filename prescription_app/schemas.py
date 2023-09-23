from pydantic import BaseModel
from typing import List


class Medication(BaseModel):
    name: str
    dosage: float
    frequency: str
    codes: List[str] = []


class Prescription(BaseModel):
    patient_id: int
    medications: List[str] = []
    open: bool
