import requests
from dao.medication_cache import MedicationCache
from payload_validation import MedicationPayload
from schemas import Medication
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

    def getMedicationIfExists(self, name: str):
        # check if the medication exists in cache
        medication = self.medication_cache.get(name)
        if medication:
            return medication

        # check if exists in medications dao and if so promote to cache
        medication = self.medications.get(name)
        if medication:
            self.medication_cache.create(medication)
            return medication

    def fetchMedication(self, medication: MedicationPayload):
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

    def addMedicationToPrescription(self, prescription_id: str, medication: Medication):
        existing_prescription = self.prescriptions.get(prescription_id)
        if existing_prescription:
            existing_prescription.medications.append(medication.name)
            return medication.name
        return None

    def add_medication(self, prescription_id: str, medication: MedicationPayload):
        existing_medication = self.getMedicationIfExists(medication.name)
        if existing_medication:
            medication_name = self.addMedicationToPrescription(
                prescription_id, existing_medication
            )
            if not medication_name:
                return (
                    f"Error when trying to add {medication.name} to prescription {prescription_id}",
                    500,
                )
            return (
                medication_name,
                200,
            )
        else:
            new_medication = self.fetchMedication(medication)
            if new_medication:
                self.medications.create(new_medication)
                self.medication_cache.create(new_medication)
                medication_name = self.addMedicationToPrescription(
                    prescription_id, new_medication
                )
                if not medication_name:
                    return (
                        f"Error when trying to add {new_medication.name} to prescription {prescription_id}",
                        500,
                    )
                return (
                    medication_name,
                    200,
                )
        return "medicationNotFound", 400
