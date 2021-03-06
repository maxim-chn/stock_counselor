from backend_tasks_api import BackendTasksApi
from datetime import datetime
from common_classes.loggable import Loggable
from sec_communicator_api import SecCommunicatorApi
from sys import getsizeof

class WorkerApi(Loggable):
  """
  An internal API for executing the backend tasks related to the financial data gathering
  """

  def __init__(self):
    super().__init__("WorkerApi")
    self._backend_tasks = BackendTasksApi()
    self._sec_communicator = SecCommunicatorApi()

  def getCompanyAcronymForGathering(self):
    """
    Returns a str with the company acronym, i.e. msft, in case there is a new backend task
    for the financial data gathering.
    Otherwise, returns None.
    """
    self._debug("getCompanyAcronymForGathering", "Start")
    result = self._backend_tasks.getAcronymOfTaskWithProgressInitiated()
    self._debug("getCompanyAcronymForGathering", "Finish - result: %s\n" % result)
    return result

  def getDataFromSec(self, acronym):
    """
    Returns a dict with the company financial data from the https://www.sec.gov/

    Keyword arguments:
      acronym -- str -- unique company acronym. For example, msft is an acronym for Microsoft
    """
    self._debug("getDataFromSec", "Start - acronym: %s" % acronym)
    result = {
      "acronym": acronym,
      "currency_units": None,
      "data_from_source": dict()
    }

    self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining company id")
    company_id = self._sec_communicator.getCompanyId(acronym)

    if company_id:
      self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining 10-K filings")
      html_document_with_10k_search_results = self._sec_communicator.get10kReportsSearchResults(
        company_id
      )

    if html_document_with_10k_search_results:
      self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining 10-K accession_numbers")
      accession_numbers = self._sec_communicator.get10kAccessionNumbers(
        html_document_with_10k_search_results
      )

    if accession_numbers:
      self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining 10-K financial statements ids")

      pivot_date = datetime.strptime("2015-01-01", '%Y-%m-%d')
      for date_str, accession_number in accession_numbers.items():
        next_date = datetime.strptime(date_str, '%Y-%m-%d')

        if next_date < pivot_date:
          continue

        html_document_with_10k_report = self._sec_communicator.get10KReport(
          company_id,
          accession_number
        )

        if html_document_with_10k_report:
          income_statements_ids = self._sec_communicator.getFinancialStatementsIds(
            html_document_with_10k_report
          )

          result["data_from_source"][date_str] = dict()
          for income_statement_id in income_statements_ids:
            self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining data from financial statement")
            html_document_with_financial_statement = self._sec_communicator.getFinancialStatement(
              company_id,
              accession_number,
              income_statement_id
            )

            if html_document_with_financial_statement:
              financial_data = self._sec_communicator.getDataFromFinancialStatement(
                html_document_with_financial_statement
              )

              if not result["currency_units"] and financial_data[1]:
                result["currency_units"] = financial_data[1]

              result["data_from_source"][date_str] = result["data_from_source"][date_str] | financial_data[0]

    self._debug("getDataFromSec", "Finish - result: %d bytes\n" % getsizeof(result))
    return result
