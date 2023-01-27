"""
Retrieves and transforms World Bank data for risk scoring analysis.

This module, contains one main class ``RiskScoringDataPreparator`` that implements
``prepare_indicators_data`` method for `Wold bank` indicators data retrieval and 
transformation for further risk scoring analyses.
Note that, for this version, the module is mainly used to assist Methane emissions 
risk scoring analysis, but can be used for other  `Wold bank` indicators data preparation.
"""

import pandas as pd
from services.utils import *
from services.scrappers import *
from .utils import get_set_of_all_countries_alpha2_code


class RiskScoringDataPreparator:
    """
    Prepares data for risk scoring analysis.

    Parameters
    ----------
    main_indicator_id: str
        Identifier of indicator of interest for which we want to construct risk
        scores.
    imputation_indicators_ids: tuple
        tuple of identifiers of indicators which could be used later on for
    multivariate imputation to improve the main indicator missing data estimation.
    """

    def __init__(self, main_indicator_id: str,
                 imputation_indicators_ids: tuple):
        self._main_indicator_id = main_indicator_id
        self._imputation_indicators_ids = imputation_indicators_ids
        self._full_df = None

    @property
    def main_indicator_id(self):
        return self._main_indicator_id

    @property
    def imputation_indicators_ids(self):
        return self._imputation_indicators_ids

    @property
    def full_df(self):
        return self._full_df

    @full_df.setter
    def full_df(self, value):
        self._full_df = value

    def prepare_indicators_data(self):
        """
        Generates the final risk scores of all countries
        for all available years.
        """
        self.setup_indicators_full_dataframe()
        self.keep_actual_countries_records_only()

    def setup_indicators_full_dataframe(self):
        """
        Set up the dataframe with the all indicators retrieved data of interest.
        """
        indicators_dfs = [self.get_indicator_dataframe(self.main_indicator_id)]
        for indicator_id in self.imputation_indicators_ids:
            indicators_dfs.append(
                self.get_indicator_dataframe(indicator_id,
                                             drop_index=True,
                                             drop_columns=["country_name"]))
        self.full_df = pd.concat(indicators_dfs, axis=1, join="inner")

    def get_indicator_dataframe(self,
                                indicator_id: str,
                                drop_index: bool = False,
                                drop_columns: list = None):
        """
        Retrieve and format indicator data in a dataframe
        """
        indicator_records = self.get_indicator_data(indicator_id)
        formated_indicator_records = list(
            map(self.get_formatted_indicator_record, indicator_records))
        indicator_df = pd.DataFrame(formated_indicator_records)
        indicator_df.set_index(["country_id", "date"],
                               inplace=True,
                               drop=drop_index)
        if drop_columns:
            indicator_df.drop(drop_columns, axis=1, inplace=True)
        return indicator_df

    def get_indicator_data(self, indicator_id: str):
        """
        Strap indicator data given `indicator_id`
        """
        indicator_data = WorldBankAPIDataScrapper.get_all_indicator_data(
            indicator_id)
        indicator_records = indicator_data[1]
        return indicator_records

    @staticmethod
    def get_formatted_indicator_record(record: dict):
        """
        Map and filter API retrieved `record` for a given indicator
        to match a desired object format for later easier
        data transformations
        """
        indicator_id = record['indicator']['id']
        new_format_record = {
            "country_id": record["country"]["id"],
            "country_name": record["country"]["value"],
            "date": record["date"],
            indicator_id: record["value"],
        }
        return new_format_record

    def keep_actual_countries_records_only(self):
        """
        Removes records of non country data
        (Examples or removed country identifiers: South Asia, Upper middle income...etc.)
        """
        country_alpha2_codes = get_set_of_all_countries_alpha2_code()
        drop_condition = self.full_df is not None and "country_id" in self.full_df.columns
        if drop_condition:
            current_country_ids = self.full_df.country_id.unique()
            country_ids_to_keep = [
                id_ for id_ in current_country_ids
                if id_ in country_alpha2_codes
            ]
            self.full_df = self.full_df.loc[country_ids_to_keep]
