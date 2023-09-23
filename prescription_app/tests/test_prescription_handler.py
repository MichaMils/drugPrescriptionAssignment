from unittest.mock import  Mock
import pytest
from uuid import UUID
from prescription_handler import PrescriptionHandler  # Import your PrescriptionHandler class
from dao.prescription_dao import PrescriptionDAO
from dao.medication_dao import MedicationDAO
from schemas import Prescription, Medication


# Define fixtures to set up objects for testing
@pytest.fixture
def prescription_dao():
    return PrescriptionDAO()


@pytest.fixture
def medication_dao():
    return MedicationDAO()


@pytest.fixture
def prescription_handler(prescription_dao, medication_dao):
    return PrescriptionHandler(prescription_dao, medication_dao)

existing_medication1 = Medication(name="ExistingMed", dosage=2.5, frequency="daily", codes=["731531"])
existing_medication2 = Medication(name="ExistingMed", dosage=2.5, frequency="daily", codes=["1790679"])
existing_medications = [existing_medication1, existing_medication2]

# Test the create_prescription method
def test_create_prescription(prescription_handler):
    patient_id = 123
    prescription_id = prescription_handler.create_prescription(patient_id)

    # Verify that the prescription ID is a valid UUID
    assert isinstance(UUID(prescription_id), UUID)

    # Retrieve the created prescription from the DAO and assert its properties
    created_prescription = prescription_handler.prescriptions.get(prescription_id)
    assert created_prescription.patient_id == patient_id
    assert created_prescription.open is True

def get_medication_mock(*args, **kwargs):
    return existing_medications.pop()

@pytest.mark.asyncio
async def test_close_prescription(prescription_handler,prescription_dao, medication_dao):
    # Create a prescription (replace with your actual test data)
    patient_id = 123
    prescription_id = "123"
    existing_prescription = Prescription(id=prescription_id, patient_id=patient_id, medications=["Medication1", "Medication2"])
    prescription_dao.get = Mock(return_value=existing_prescription)
    medication_dao.get = Mock(side_effect=get_medication_mock)
    # Define a mock response that simulates the warnings output
    expected_response = {
        "warnings": [
            {
                "codes": ("1790679", "731531"),
                "warning": [
                    "Drug1 (rxcui = 1790679, name = simvastatin 4 MG/ML Oral Suspension, tty = SCD). Drug2 (rxcui = 731531, name = ibuprofen 40 MG/ML Oral Suspension [Advil], tty = SBD). Drug1 is resolved to simvastatin, Drug2 is resolved to ibuprofen and interaction asserted in DrugBank between Simvastatin and Ibuprofen."
                ],
            },
        ],
    }


    # Close the prescription and get the warnings
    warnings = await prescription_handler.close_prescription(prescription_id)

    # Assertions for the warnings (modify as needed based on your expected warnings)
    assert isinstance(warnings, list)
    assert len(warnings) == len(expected_response["warnings"])

    for actual_warning, expected_warning in zip(warnings, expected_response["warnings"]):
        assert actual_warning == expected_warning
