from schemas import Medication


class MedicationDAO:
    def __init__(self):
        self.medications = {}

    def create(self, medication: Medication):
        self.medications[medication.name] = medication
        return medication.name

    def update(self, medication_name: str, updated_medication: Medication):
        if medication_name not in self.medications:
            return None
        self.medications[medication_name] = updated_medication

    def delete(self, medication_name: str):
        if medication_name not in self.medications:
            return None
        del self.medications[medication_name]

    def get(self, medication_name: str):
        if medication_name not in self.medications:
            return None
        return self.medications[medication_name]
