"""
MongoDB Database controller module for the Methane emissions scores .py

This module contains one main class ``RiskScoresDbController`` that implements methods
for records insertion (`insert_record`) and query (`get_record_by_fields`)
"""

from pymongo import MongoClient
from models import MethaneScoreDocumentModel


class RiskScoresDbController:
    """
    Connects to MongoDB database and performs query operations
    on the Methane scores collection. 
    """
    db_client = MongoClient("mongodb://127.0.0.1:27017/")
    db = db_client.riskScoresDb

    @classmethod
    def insert_record(cls, record: MethaneScoreDocumentModel):
        """
        Inserts a methane score record to the `riskScoresDb` 
        collection
        """
        cls.db.methaneScores.insert_one(record.dict())

    @classmethod
    def get_record_by_fields(cls, fields: dict):
        """
        Get a record given a list of filter fields
        """
        projection = {"_id": 0}
        return cls.db.methaneScores.find_one(fields, projection=projection)
