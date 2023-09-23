from abc import ABC, abstractmethod
from typing import List

from schemas import Prescription


class Validator(ABC):
    @abstractmethod
    async def validate(self, prescription: Prescription) -> List[str]:
        pass
