"""
Implements an API scrapper of the World bank API.

This module contains one main class ``WorldBankAPIDataScrapper`` that
implements methods to retrieve data of interest from the World bank 
sources. For now, the class allows to retrieve countries and indicators data.
"""

import requests
from ..utils import handle_third_part_error


class WorldBankAPIDataScrapper:
    """
    Scrapper to retrieve data of interest from the World bank API
    """

    API_BASE_URL = "https://api.worldbank.org/v2"
    API_TIMEOUT = 3000

    @classmethod
    def get_all_countries_data(cls, source_id=2):
        """
        Get all countries data
        """
        url = f"{cls.API_BASE_URL}/country"
        records_total_number = cls.get_total_number_of_records(
            url, source_id=source_id)
        query_params = {"per_page": records_total_number, "source": source_id}
        return cls.get_json_response(url, query_params)

    @classmethod
    def get_all_indicator_data(cls, indicator_id, source_id=2):
        """
        Get all countries indicator data for all years
        """
        url = f"{cls.API_BASE_URL}/country/all/indicators/{indicator_id}"
        records_total_number = cls.get_total_number_of_records(url, source_id)
        query_params = {"per_page": records_total_number, "source": source_id}
        return cls.get_json_response(url, query_params)

    @classmethod
    def get_total_number_of_records(cls, url, source_id):
        """
        Returns the total number of available records in the API ressource
        """
        query_params = {"per_page": 1, "source": source_id}
        response = cls.get_json_response(url, query_params)
        metadata = response[0]
        total = metadata.get("total", None)
        if total is None:
            raise ValueError("Error retrieving total number of records")
        return metadata.get("total", None)

    @classmethod
    @handle_third_part_error
    def get_json_response(cls, url, query_params):
        """
        Runs a query given the `url` and `query_params`

        Returns response in json format.
        """
        query_params["format"] = "json"
        response = requests.get(url,
                                params=query_params,
                                timeout=cls.API_TIMEOUT)
        return response.json()
