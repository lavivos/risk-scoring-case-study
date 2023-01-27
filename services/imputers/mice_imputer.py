import pandas as pd

from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

from .base_imputer import BaseImputer


class MiceImputer(BaseImputer):

    def __init__(self, dataframe, imputer_params=None):
        super().__init__(dataframe, imputer_params)

    def impute(self):
        self.scale()
        self.imputer = IterativeImputer(**self.imputer_params)
        self.imputed_df = self.imputer.fit_transform(self.scaled_df)
        self.imputed_df = pd.DataFrame(
            self.scaler.inverse_transform(self.imputed_df),
            columns=[column for column in self.dataframe.columns])
