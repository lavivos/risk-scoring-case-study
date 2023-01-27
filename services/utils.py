"""
Utilities functions module.
"""

import json
import requests
import pycountry
from fastapi import HTTPException


def handle_third_part_error(func):
    """
    Handle `worldbank` 3rd party api errors
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as exception:
            raise HTTPException(
                status_code=500,
                detail=f"Error from Wold Bank third-party API: {exception}"
            ) from exception

    return inner


def save_data_to_json(data: dict, filename: str):
    """
    Save data to JSON file in the server's data directory
    """
    with open(f"./data/{filename}.json", "w+") as file:
        json.dump(data, file)


def load_data_from_json(filename: str):
    """
    Load data from the server's data directory
    """
    with open(f"./data/{filename}.json", "r") as f:
        loaded_data = json.load(f)
    return loaded_data


def get_set_of_all_countries_alpha2_code():
    """
    returns the set of alpha 2 codes of all countries
    """
    return {country.alpha_2 for country in pycountry.countries}
