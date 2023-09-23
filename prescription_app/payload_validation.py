from pydantic import BaseModel


class MedicationPayload(BaseModel):
    name: str
    dosage: float
    frequency: str
