# risk-scoring-project:

The project answers the case study requirements in two major parts:

- The notebook (`Methane-Risk-Score-Notebook.ipynb`): Goes through all the questions, using the developed `services` package modules necessary to handle each question in addition to third party libraries. Using a notebook provides easier evaluation of the answers to all questions, instead of using modules and packages for each question.

`Note`: Please note that for the project at hand, this notebook provides also the script for processed data storage to a MongoDB database, that is intended to store the records of risk scores and metadata used by the API.

- The API: Provides a simple implementation of the required FastAPI for serving risk scores of Methane emissions. It is mainly composed of the packages `api` and `models`.

`Note`: `services` package was mainly used outside the API to prepare final data. This is done for performance reasons, by avoiding the lenghty processing and computation of risk scores by end users when using the API.
