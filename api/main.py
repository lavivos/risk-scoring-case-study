"""
Main risk  scoring API module.

This version of the API implements one endpoint for the
Methane emissions indicator only.
"""

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from typing import Optional

from .db import RiskScoresDbController

app = FastAPI()


@app.get("/indicators/methane-emissions/{alpha2code}")
async def get_methane_risk_score_info(alpha2code: str,
                                      year: Optional[int] = Query(None)):
    """
    Returns data and metadata on methane emissions risk score
    for a given country (`alpha2code`) and `year`.

    Parameters
    ----------
    alpha2code: alpha2 code country identifier.

    Note
    ----
    Given that the `year` is optional, we will return first record
    matching the country identifier.
    """
    query_fields = {"alpha2code": alpha2code}
    if year:
        query_fields.update({"year": year})
    loaded_response = RiskScoresDbController.get_record_by_fields(query_fields)
    if loaded_response is None:
        return JSONResponse(content={"message": "No record found"},
                            status_code=404)
    return loaded_response
