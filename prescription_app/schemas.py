from pydantic import BaseModel
from typing import List

class MedicationPayload(BaseModel):
    name: str
    dosage: float
    frequency: str

class Medication(BaseModel):
    name: str
    dosage: float
    frequency: str
    codes: List[str] = []

class Prescription(BaseModel):
    id: str
    patient_id: int
    medications: List[str] = []
    open: bool = True
