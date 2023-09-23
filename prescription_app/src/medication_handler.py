import requests
from dao.medication_cache import MedicationCache
from schemas import Medication, MedicationPayload
from dao.prescription_dao import PrescriptionDAO
from dao.medication_dao import MedicationDAO

class MedicationHandler:
    def __init__(
        self,
        prescriptions: PrescriptionDAO,
        medications: MedicationDAO,
        medication_cache: MedicationCache,
    ) -> None:
        self.prescriptions = prescriptions
        self.medications = medications
        self.medication_cache = medication_cache

    def get_medication_if_exists(self, name: str):
        medication = self.medication_cache.get(name)
        if medication:
            return medication

        # check if exists in medications dao and if so promote to cache
        medication = self.medications.get(name)
        if medication:
            self.medication_cache.create(medication)
            return medication

    def fetch_medication(self, medication: MedicationPayload):
        try:
            res = requests.get(
                f"https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?terms={medication.name}&ef=RXCUIS"
            )
            data = res.json()
        except Exception as e:
            data = None
        if not data:
            return None
        value, medicines, codes, medicines_list = data
        if len(medicines) == 0:
            return

        # assumption there is only one matching medicine with the given name.
        for i in range(len(medicines)):
            if medicines[i] == medication.name:
                medication_codes = codes["RXCUIS"][i]
                medication_data = {
                    "name": medication.name,
                    "dosage": medication.dosage,
                    "frequency": medication.frequency,
                    "codes": medication_codes,
                }
                new_medication = Medication(**medication_data)
                return new_medication

    def add_medication_to_prescription(self, prescription_id: str, medication: Medication):
        existing_prescription = self.prescriptions.get(prescription_id)
        if existing_prescription:
            existing_prescription.medications.append(medication.name)
            return (medication.name,200,)
        return (
            f"Invalid prescription id, error when trying to add {medication.name} to prescription {prescription_id}",
            400,
            )

    def add_medication(self, prescription_id: str, medication: MedicationPayload):
        existing_medication = self.get_medication_if_exists(medication.name)
        if existing_medication:
            return self.add_medication_to_prescription(prescription_id, existing_medication)
        else:
            new_medication = self.fetch_medication(medication)
            if new_medication:
                self.medications.create(new_medication)
                self.medication_cache.create(new_medication)
                return self.add_medication_to_prescription(prescription_id, new_medication)
        return "Medication not found!", 404
