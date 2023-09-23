from schemas import Prescription
from dao.prescription_dao import PrescriptionDAO
from dao.medication_dao import MedicationDAO
from validators.prescription_validator import PrescriptionValidator
import uuid


class PrescriptionHandler:
    def __init__(
        self, prescriptions: PrescriptionDAO, medications: MedicationDAO
    ) -> None:
        self.prescriptions = prescriptions
        self.prescription_validator = PrescriptionValidator(prescriptions, medications)

    def create_prescription(self, patient_id):
        prescription_id = str(uuid.uuid4())
        prescription_data = {
            "id": prescription_id,
            "patient_id": patient_id
        }
        prescription = Prescription(**prescription_data)
        prescription_id = self.prescriptions.create(prescription)
        return prescription_id

    async def close_prescription(self, prescription_id):
        warnings = await self.prescription_validator.validate(prescription_id)
        if not warnings:
            return None
        return warnings
