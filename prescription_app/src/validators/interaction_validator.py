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
    ):
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

        return interaction_results

    def extract_comments(self, data):
        # Extract and return interaction information from the API response
        full_interaction_type_group = data.get("fullInteractionTypeGroup", None)
        if full_interaction_type_group:
            interaction_raw_data = full_interaction_type_group[0].get(
                "fullInteractionType", None
            )
            if interaction_raw_data:
                return [
                    interaction.get("comment")
                    for interaction in interaction_raw_data
                ]

    async def fetch_interaction(self, session, codes: Tuple[str]):
        # Construct the API URL with the provided codes
        api_url = f"{self.api_base_url}?rxcuis={'+'.join(codes)}"

        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                return {'codes': codes, 'warning': self.extract_comments(data)}
            # Handle API request errors or non-200 responses
            return {}

    async def validate(self, prescription: Prescription) -> List[str]:
        medicine_codes = self.get_medicine_codes(prescription)

        async with aiohttp.ClientSession() as session:
            interaction_results = await self.get_interactions(session, medicine_codes)

        return interaction_results
