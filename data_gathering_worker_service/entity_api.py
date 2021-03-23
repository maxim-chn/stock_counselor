from common.loggable_api import Loggable
from json import dump
from os import path

class Entity(Loggable):
  """
  This is our Entity Logic.
  It accesses the database records.
  TODO: remove in v1.0 the use of file system and integrate a database, i.e. MongoDb.
  """

  def __init__(self, log_id):
    """
    Keyword arguments:
      log_id -- str.
    """
    super().__init__(log_id, "Entity")

  def storeFinancialData(self, data):
    """
    Persists the financial data for a company.
    Keyword arguments:
      data -- dict -- an object with the financial details for a company.
    """
    path_to_storage_file = self._getCompanyFinancialDataStoragePath(self, data["acronym"])
    with open(path_to_storage_file, "w+") as write_file:
      dump(data, write_file)


  def _getCompanyFinancialDataStoragePath(self, company_acronym):
    """
    TODO: remove in v1.0
    Returns a path.
    It is the location to the storage file for the company's financial data.
    Keyword arguments:
      company_acronym -- str -- the company symbol at the stock exchange, i.e. NASDAQ.
    """
    return path.join(
      path.dirname(__file__),
      "..",
      "common",
      "financial_data_db",
      "%s.json" % company_acronym
    )