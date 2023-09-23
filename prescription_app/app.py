from flask import Flask, jsonify, request, abort
from medication_handler import MedicationHandler
from prescription_handler import PrescriptionHandler
from schemas import MedicationPayload
from dao.medication_cache import MedicationCache
from dao.prescription_dao import PrescriptionDAO
from dao.medication_dao import MedicationDAO
from pydantic import ValidationError
import logging, sys


app = Flask(__name__)

medication_model = MedicationPayload
prescriptions = PrescriptionDAO()
medications = MedicationDAO()
medication_cache = MedicationCache()
prescriptionHandler = PrescriptionHandler(prescriptions, medications)
medicationHandler = MedicationHandler(prescriptions, medications, medication_cache)


@app.route("/", methods=["GET"])
def health_check():
    app.logger.info("App is live and running!")
    return "Alive!"


@app.route("/open_prescription/<int:patient_id>", methods=["POST"])
def open_prescription(patient_id):
    prescription_id = prescriptionHandler.create_prescription(patient_id)
    return jsonify({"prescription_id": prescription_id}), 201


@app.route("/get_medications", methods=["GET"])
def get_medications():
    return jsonify({"medications": medications.medications})


# @app.route("/get_prescriptions", methods=["GET"])
# def get_prescriptions():
#     return jsonify(
#         {
#             "prescriptions": [
#                 prescription.to_json()
#                 for prescription in prescriptions.prescriptions.values()
#             ]
#         }
#     )


@app.route("/add_medication/<string:prescription_id>", methods=["POST"])
def add_medication_to_prescription(prescription_id):
    try:
        medication = medication_model(**request.get_json())
    except ValidationError as e:
        abort(400, str(e))

    # check if the prescription is valid
    existing_prescription = prescriptions.get(prescription_id)
    if not existing_prescription:
        return jsonify({"message": f"Prescription {prescription_id} not found"})

    # check if medications can be added to the prescription
    if not existing_prescription.open:
        return jsonify(
            {"message": f"Prescription {prescription_id} is closed already!"}
        )

    message, status_code = medicationHandler.add_medication(prescription_id, medication)
    return jsonify({"message": message}), status_code


@app.route("/close_prescription/<string:prescription_id>", methods=["POST"])
async def close_prescription(prescription_id):
    warnings = await prescriptionHandler.close_prescription(prescription_id)
    if warnings:
        return jsonify({"warnings": warnings}), 400
    prescription = prescriptions.get(prescription_id)
    prescription.open = False
    prescriptions.update(prescription_id, prescription)
    return jsonify({"message": "Prescription closed successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3001)
