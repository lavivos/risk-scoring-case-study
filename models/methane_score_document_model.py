# -*- coding: utf-8 -*-
"""
Implements Methane risk score document model in the database
"""

from pydantic import BaseModel


class MethaneScoreDocumentModel(BaseModel):
    alpha2code: str
    year: int
    value: float
    value_uncertainty: float
    estimated: bool
    country_name: str
    score_index: int
