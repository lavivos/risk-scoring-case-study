"""
Interface for data imputation algorithms.
"""

from abc import ABC, abstractmethod
from sklearn.preprocessing import StandardScaler


class BaseImputer(ABC):
    """
    Implements the interface for data imputation algorithms.

    Parameters
    ----------
    dataframe: pandas dataframe
        Contains the data with missing values.
    imputer_params: dict
        Contains imputation algorithm parameters

    Note:
    ----
    For the current implementation, this module expects numeric features only.
    Integration of other types of features (categorical, date) is not supported.
    """

    def __init__(self, dataframe, imputer_params=None):
        self._dataframe = dataframe
        self.imputer_params = imputer_params
        if imputer_params is None:
            self.imputer_params = {}
        self.imputed_df = None
        self.scaled_df = None
        self.imputer = None
        self.scaler = None

    @property
    def dataframe(self):
        return self._dataframe

    @dataframe.setter
    def dataframe(self, value):
        self._dataframe = value

    @abstractmethod
    def impute(self):
        """
        Abstract method that applies the imputation.
        
        Updates `imputed_df` attribute
        """

    def scale(self):
        """
        Scales the data
        """
        self.scaler = StandardScaler()
        self.scaled_df = self.scaler.fit_transform(self.dataframe)
