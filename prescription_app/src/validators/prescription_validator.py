import asyncio
from dao.prescription_dao import PrescriptionDAO
from dao.medication_dao import MedicationDAO
from schemas import Prescription
from validators.always_valid_validator import AlwaysValid
from validators.interaction_validator import InteractionValidator
from typing import List


class PrescriptionValidator:
    def __init__(self, prescriptions: PrescriptionDAO, medications: MedicationDAO):
        self.validators = [InteractionValidator(medications), AlwaysValid()]
        self.prescriptions = prescriptions

    async def validate(self, prescription: Prescription) -> List[str]:
        # Use asyncio.gather to run all validators asynchronously
        results = await asyncio.gather(
            *[validator.validate(prescription) for validator in self.validators]
        )

        # Concatenate the results from all validators
        all_warnings = []
        for warning_list in results:
            all_warnings.extend(warning_list)

        return all_warnings
