from schemas import Medication


class MedicationCache:
    def __init__(self) -> None:
        self.cache = {}

    def create(self, medication: Medication):
        self.cache[medication.name] = medication
        return medication.name

    def update(self, medication_name: str, updated_medication: Medication):
        if medication_name not in self.cache:
            raise KeyError(f"Medication with ID {medication_name} not found.")
        self.cache[medication_name] = updated_medication

    def delete(self, medication_name: str):
        if medication_name not in self.cache:
            raise KeyError(f"Medication with ID {medication_name} not found.")
        del self.cache[medication_name]

    def get(self, medication_name: str):
        if medication_name not in self.cache:
            return None
        return self.cache[medication_name]
