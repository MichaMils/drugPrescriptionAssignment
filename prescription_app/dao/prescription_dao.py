from schemas import Prescription


class PrescriptionDAO:
    def __init__(self):
        self.prescriptions = {}

    def create(self, prescription: Prescription):
        self.prescriptions[prescription.id] = prescription
        return prescription.id

    def update(self, prescription_id: str, updated_prescription: Prescription):
        if prescription_id not in self.prescriptions:
            raise KeyError(f"Prescription with ID {prescription_id} not found.")
        self.prescriptions[prescription_id] = updated_prescription

    def delete(self, prescription_id: str):
        if prescription_id not in self.prescriptions:
            raise KeyError(f"Prescription with ID {prescription_id} not found.")
        del self.prescriptions[prescription_id]

    def get(self, prescription_id: str) -> Prescription:
        if prescription_id not in self.prescriptions:
            return None
        return self.prescriptions[prescription_id]
