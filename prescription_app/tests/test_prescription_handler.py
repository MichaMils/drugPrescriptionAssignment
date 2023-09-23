from unittest.mock import  Mock, patch
import pytest
from uuid import UUID
from prescription_handler import PrescriptionHandler  # Import your PrescriptionHandler class
from dao.prescription_dao import PrescriptionDAO
from dao.medication_dao import MedicationDAO


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


@pytest.mark.asyncio
async def test_close_prescription(prescription_handler):
    # Create a prescription (replace with your actual test data)
    patient_id = 123
    prescription_id = prescription_handler.create_prescription(patient_id)

    # Define a mock response that simulates the warnings output
    mock_response_data = {
        "warnings": [
            {
                "codes": ["731531", "1790679"],
                "warning": [
                    "Drug1 (rxcui = 1790679, name = simvastatin 4 MG/ML Oral Suspension, tty = SCD). Drug2 (rxcui = 731531, name = ibuprofen 40 MG/ML Oral Suspension [Advil], tty = SBD). Drug1 is resolved to simvastatin, Drug2 is resolved to ibuprofen and interaction asserted in DrugBank between Simvastatin and Ibuprofen."
                ],
            },
            # Add more warnings as needed
        ],
    }

    # Create a mock response with the JSON data
    mock_response = Mock()
    mock_response.json.return_value = mock_response_data

    # Mock the requests.get method to return the mock response
    with patch('requests.get', return_value=mock_response):
        # Close the prescription and get the warnings
        warnings = await prescription_handler.close_prescription(prescription_id)

    # Assertions for the warnings (modify as needed based on your expected warnings)
    assert isinstance(warnings, list)
    assert len(warnings) == len(mock_response_data["warnings"])

    for actual_warning, expected_warning in zip(warnings, mock_response_data["warnings"]):
        assert actual_warning == expected_warning
