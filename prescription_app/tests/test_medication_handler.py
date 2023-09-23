import pytest
from unittest.mock import Mock
import unittest.mock as mock
from schemas import Medication, MedicationPayload, Prescription
from dao.medication_cache import MedicationCache
from dao.prescription_dao import PrescriptionDAO
from dao.medication_dao import MedicationDAO
from medication_handler import MedicationHandler


@pytest.fixture
def prescription_dao():
    return PrescriptionDAO()


@pytest.fixture
def medication_dao():
    return MedicationDAO()


@pytest.fixture
def medication_cache():
    return MedicationCache()


@pytest.fixture
def medication_handler(prescription_dao, medication_dao, medication_cache):
    return MedicationHandler(prescription_dao, medication_dao, medication_cache)


def test_getMedicationIfExists_existing_medication(medication_cache, medication_handler):
    # Mock the MedicationCache.get method to return an existing medication
    medication_cache.get = Mock(return_value=Medication(name="ExistingMed", dosage=2.5, frequency="daily"))

    # Test the getMedicationIfExists method
    result = medication_handler.getMedicationIfExists("ExistingMed")

    assert result.name == "ExistingMed"


def test_getMedicationIfExists_non_existing_medication(medication_cache, medication_dao, medication_handler):
    # Mock the MedicationCache.get method to return None (medication not found)
    medication_cache.get = Mock(return_value=None)

    # Mock the MedicationDAO.get method to return None (medication not found)
    medication_dao.get = Mock(return_value=None)

    # Test the getMedicationIfExists method
    result = medication_handler.getMedicationIfExists("NonExistingMed")

    assert result is None


@mock.patch('requests.get')
def test_fetchMedication_valid_data(requests_get_mock, medication_handler):
    mock_response = Mock()
    mock_response.json.return_value = ("value", ["someMedication"], {"RXCUIS": [["123456"]]}, ["MedicationName"])
    requests_get_mock.return_value = mock_response
    medication_payload = MedicationPayload(name="someMedication", dosage=2.5, frequency="daily")
    result = medication_handler.fetchMedication(medication_payload)

    assert result.name == "someMedication"
    assert result.dosage == 2.5
    assert result.frequency == "daily"
    assert result.codes == ["123456"]


@mock.patch('requests.get')
def test_fetchMedication_invalid_data(requests_get_mock, medication_handler):
    # Mock the requests.get method to return invalid data (empty response)
    mock_response = mock.Mock()
    mock_response.json.return_value = None
    # requests_get_mock = Mock(return_value=mock_response)
    requests_get_mock.return_value = mock_response

    # Test the fetchMedication method with invalid data
    medication_payload = MedicationPayload(name="NonExistingMedication", dosage=2.5, frequency="daily")
    result = medication_handler.fetchMedication(medication_payload)

    assert result is None


def test_addMedicationToPrescription_existing_prescription(prescription_dao, medication_handler):
    # Mock an existing prescription in the DAO
    existing_prescription = Prescription(id="123", patient_id=1, medications=["Medication1"])
    prescription_dao.get = Mock(return_value=existing_prescription)

    # Test the addMedicationToPrescription method with an existing prescription
    medication = Medication(name="Medication2", dosage=2.0, frequency="twice daily")
    result = medication_handler.addMedicationToPrescription("123", medication)

    assert result == "Medication2"


def test_add_medication_existing_medication(medication_cache, medication_handler):
    # Mock an existing medication in the cache
    existing_medication = Medication(name="Medication1", dosage=2.5, frequency="daily")
    medication_cache.get = Mock(return_value=existing_medication)

    # Mock the addMedicationToPrescription method to return a success message
    medication_handler.addMedicationToPrescription = Mock(return_value="Success")

    # Test the add_medication method with an existing medication
    medication_payload = MedicationPayload(name="Medication1", dosage=2.5, frequency="daily")
    result, status_code = medication_handler.add_medication("123", medication_payload)

    assert result == "Success"
    assert status_code == 200


def test_add_medication_non_existing_medication(medication_cache,medication_dao, medication_handler):
    # Mock a non-existing medication in the cache and DAO
    medication_cache.get = Mock(return_value=None)
    medication_dao.get = Mock(return_value=None)

    # Mock the fetchMedication method to return a new medication
    new_medication = Medication(name="NewMedication", dosage=1.0, frequency="once daily")
    medication_handler.fetchMedication = Mock(return_value=new_medication)

    # Mock the addMedicationToPrescription method to return a success message
    medication_handler.addMedicationToPrescription = Mock(return_value="Success")

    # Test the add_medication method with a non-existing medication
    medication_payload = MedicationPayload(name="NewMedication", dosage=1.0, frequency="once daily")
    result, status_code = medication_handler.add_medication("123", medication_payload)

    assert result == "Success"
    assert status_code == 200
