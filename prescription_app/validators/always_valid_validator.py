from typing import List
from schemas import Prescription
from validators.validator import Validator


class AlwaysValid(Validator):
    async def validate(self, prescription: Prescription) -> List[str]:
        # This validator always returns an empty list (always valid)
        return []
