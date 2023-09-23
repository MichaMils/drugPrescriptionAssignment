# from prescription_app.dao.models import (
#     Prescription,
#     Medication
# )
# import requests

# # In-memory data store
# prescriptions = PrescriptionDAO()
# medications = MedicationDAO()
# medications_cache = {}


# def create_prescription(patient_id):
#     prescription = Prescription(patient_id)
#     prescription_id = prescriptions.create(prescription)
#     return prescription_id


# def add_medication(prescription_id, medication):
#     # check if the medication exists in cache
#     name = medication.name
#     # return name
#     medication_content = medications_cache.get(name, None)
#     if medication_content:
#         return medication_content
#     # # if not validate that exists in the api
#     res = requests.get(
#         f"https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?terms={name}&ef=RXCUIS"
#     )
#     data = res.json()
#     value, medicines, codes, medicines_list = data
#     if len(medicines) == 0:
#         return f"No medicine named: {name} exists"
#     mapper = {}
#     for i in range(len(medicines)):
#         if medicines[i] == name:
#             mapper[medicines[i]] = codes["RXCUIS"][i]
#             # always add to medications cache
#             medications_cache[medicines[i]] = codes["RXCUIS"][i]
#     codes = []
#     medication = Medication(
#         medication.name, medication.dosage, medication.frequency, codes
#     )
#     medications.create(medication, name)
#     medications_of_the_perscription = prescriptions.get(prescription_id)
#     medications_of_the_perscription.medications.append(medication)
#     print(
#         f"medications_of_the_perscription: {medications_of_the_perscription.join(',')}"
#     )
#     return medication.name


# def close_prescription(prescription_id):
#     # Add medication interaction checking logic here.
#     # get the prescription - get the medications id
#     # request for interactions and add warnings
#     warnings = []
#     return warnings
