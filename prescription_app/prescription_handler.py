from dao.models import Prescription
from dao.prescription_dao import PrescriptionDAO
from dao.medication_dao import MedicationDAO
from validators.prescription_validator import PrescriptionValidator


class PrescriptionHandler:
    def __init__(
        self, prescriptions: PrescriptionDAO, medications: MedicationDAO
    ) -> None:
        self.prescriptions = prescriptions
        self.prescription_validator = PrescriptionValidator(prescriptions, medications)

    def create_prescription(self, patient_id):
        prescription = Prescription(patient_id)
        prescription_id = self.prescriptions.create(prescription)
        return prescription_id

    async def close_prescription(self, prescription_id):
        # Add medication interaction checking logic here.
        # get the prescription - get the medications id
        # request for interactions and add warnings
        warnings = await self.prescription_validator.validate(prescription_id)
        return warnings
