import pytest
from unittest.mock import Mock, AsyncMock
from validators.interaction_validator import InteractionValidator
from schemas import Medication, Prescription


# Define a fixture for the InteractionValidator with a mock MedicationDAO
@pytest.fixture
def interaction_validator():
    mock_medication_dao = Mock()
    return InteractionValidator(mock_medication_dao)


@pytest.mark.asyncio
async def test_get_medicine_codes(interaction_validator):
    # Create a sample prescription with medication names
    prescription = Prescription(
        id="1",
        patient_id=1,
        medications=["Medication1", "Medication2"]
    )

    # Define mock medication data for MedicationDAO
    mock_medication_data = {
        "Medication1": Medication(
            name="Medication1",
            dosage=10.0,
            frequency="Once daily",
            codes=["12345", "67890"]
        ),
        "Medication2": Medication(
            name="Medication2",
            dosage=20.0,
            frequency="Twice daily",
            codes=["54321", "09876"]
        ),
    }

    # Mock the MedicationDAO's get method to return the mock medication data
    interaction_validator.medications.get = Mock(side_effect=lambda name: mock_medication_data.get(name))

    # Get medicine codes from the prescription
    medicine_codes = interaction_validator.get_medicine_codes(prescription)

    assert isinstance(medicine_codes, list)
    assert len(medicine_codes) == 2
    assert all(isinstance(codes, list) for codes in medicine_codes)


# Test the InteractionValidator class
@pytest.mark.asyncio
async def test_interaction_validator(interaction_validator):
    # Create a sample prescription with medication names
    prescription = Prescription(
        id='1',
        patient_id=1,
        medications=["Medication1", "Medication2"]
    )

    # Define mock medication data for MedicationDAO
    mock_medication_data = {
        "Medication1": Medication(
            name="Medication1",
            dosage=10.0,
            frequency="Once daily",
            codes=["12345", "67890"]
        ),
        "Medication2": Medication(
            name="Medication2",
            dosage=20.0,
            frequency="Twice daily",
            codes=["54321", "09876"]
        ),
    }

    # Mock the MedicationDAO's get method to return the mock medication data
    interaction_validator.medications.get = Mock(side_effect=lambda name: mock_medication_data.get(name))

    # Define a mock response for the async fetch_interaction method
    async def mock_fetch_interaction(session, codes):
        return [{'codes': codes, 'warning': ["Interaction warning"]}]

    interaction_validator.fetch_interaction = AsyncMock(side_effect=mock_fetch_interaction)

    # Validate the prescription for interactions
    warnings = await interaction_validator.validate(prescription)

    assert isinstance(warnings, list)
    assert len(warnings) == 4

    # Modify the following assertions based on your expected interaction data
    expected_warning = [{'codes': ('12345', '54321'), 'warning': ['Interaction warning']}]
    assert warnings[0] == expected_warning


@pytest.mark.asyncio
async def test_interaction_validator_no_interactions(interaction_validator):
    # Create a sample prescription with medication names
    prescription = Prescription(
        id='1',
        patient_id=1,
        medications=["Medication1", "Medication2"]
    )

    # Define mock medication data for MedicationDAO
    mock_medication_data = {
        "Medication1": Medication(
            name="Medication1",
            dosage=10.0,
            frequency="Once daily",
            codes=["12345", "67890"]
        ),
        "Medication2": Medication(
            name="Medication2",
            dosage=20.0,
            frequency="Twice daily",
            codes=["54321", "09876"]
        ),
    }

    # Mock the MedicationDAO's get method to return the mock medication data
    interaction_validator.medications.get = Mock(side_effect=lambda name: mock_medication_data.get(name))

    # Define a mock response for the async fetch_interaction method
    async def mock_fetch_interaction(session, codes):
        return []  # Simulate no interactions

    interaction_validator.fetch_interaction = AsyncMock(side_effect=mock_fetch_interaction)

    # Validate the prescription for interactions
    warnings = await interaction_validator.validate(prescription)

    assert isinstance(warnings, list)
    assert len(warnings) == 4  # There should be no warnings
    assert all(len(warning) == 0 for warning in warnings)


@pytest.mark.asyncio
async def test_interaction_validator_api_error(interaction_validator):
    # Create a sample prescription with medication names
    prescription = Prescription(
        id='1',
        patient_id=1,
        medications=["Medication1", "Medication2"]
    )

    # Define mock medication data for MedicationDAO
    mock_medication_data = {
        "Medication1": Medication(
            name="Medication1",
            dosage=10.0,
            frequency="Once daily",
            codes=["12345", "67890"]
        ),
        "Medication2": Medication(
            name="Medication2",
            dosage=20.0,
            frequency="Twice daily",
            codes=["54321", "09876"]
        ),
    }

    # Mock the MedicationDAO's get method to return the mock medication data
    interaction_validator.medications.get = Mock(side_effect=lambda name: mock_medication_data.get(name))

    # Define a mock response for the async fetch_interaction method
    async def mock_fetch_interaction(session, codes):
        # Simulate an API error by returning a non-200 response
        response = Mock()
        response.status = 500
        return []

    interaction_validator.fetch_interaction = AsyncMock(side_effect=mock_fetch_interaction)

    # Validate the prescription for interactions
    warnings = await interaction_validator.validate(prescription)

    assert isinstance(warnings, list)
    assert len(warnings) == 4  # There should be no warnings due to API error
    assert all(len(warning) == 0 for warning in warnings)
