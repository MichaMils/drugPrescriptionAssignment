import asyncio
from itertools import product
from dao.medication_dao import MedicationDAO
from schemas import Prescription
from validators.validator import Validator
from typing import List, Tuple
import aiohttp


class InteractionValidator(Validator):
    def __init__(self, medications: MedicationDAO):
        self.medications = medications
        self.api_base_url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json"

    def get_medicine_codes(self, prescription: Prescription) -> List[List[str]]:
        medicine_codes_list = []

        # Iterate through the medications in the prescription
        for medication_name in prescription.medications:
            medication = self.medications.get(medication_name)

            # If the medication is found in the DAO, get its codes
            if medication:
                codes = medication.codes.copy()
                medicine_codes_list.append(codes)
            else:
                # Medication not found, add an empty list - TODO maybe better to raise exception here
                medicine_codes_list.append([])

        return medicine_codes_list

    async def get_interactions(
        self, session, medicine_codes: List[List[str]]
    ) -> List[str]:
        interactions = []
        # Use itertools.product to generate all possible combinations
        medicine_codes_combinations = list(product(*medicine_codes))

        # Call the API for interactions asynchronously for all combinations
        async with session:
            interaction_results = await asyncio.gather(
                *[
                    self.fetch_interaction(session, codes)
                    for codes in medicine_codes_combinations
                ]
            )

            # Extract interaction information from the API responses
            interactions = [
                interactions_list for interactions_list in interaction_results
            ]

        return interactions

    async def fetch_interaction(self, session, codes: Tuple[str]) -> List[str]:
        # Construct the API URL with the provided codes
        api_url = f"{self.api_base_url}?rxcuis={'+'.join(codes)}"
        print(api_url)

        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                # Extract and return interaction information from the API response - TODO
                fullInteractionTypeGroup = data.get("fullInteractionTypeGroup", None)
                if fullInteractionTypeGroup:
                    interaction_raw_data = fullInteractionTypeGroup[0].get(
                        "fullInteractionType", None
                    )
                    if interaction_raw_data:
                        return [
                            iteraction.get("comment")
                            for iteraction in interaction_raw_data
                        ]

            # Handle API request errors or non-200 responses
            return []

    async def validate(self, prescription: Prescription) -> List[str]:
        medicine_codes = self.get_medicine_codes(prescription)

        # Call the API for interactions asynchronously for all combinations
        async with aiohttp.ClientSession() as session:
            interaction_results = await self.get_interactions(session, medicine_codes)

            # Extract interaction information from the API responses
            interactions = [
                interaction
                for interactions_list in interaction_results
                for interaction in interactions_list
            ]

        return interactions
