from typing import List


class Prescription:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.medications = []  # list of strings with medications names
        self.open = True

    # def to_json(self):
    #     # Convert the Prescription object to a dictionary
    #     return {
    #         "patient_id": self.patient_id,
    #         "medications": [medication.to_dict() for medication in self.medications],
    #     }


class Medication:
    def __init__(self, name, dosage, frequency):
        self.name = name
        self.dosage = dosage
        self.frequency = frequency

    # def to_dict(self):
    #     return {"name": self.name, "dosage": self.dosage, "frequency": self.frequency}
