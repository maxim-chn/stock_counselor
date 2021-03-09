"""
It reveals an internal API for executing the backend tasks related to company data gathering
"""

from backend_tasks_api import BackendTasksApi
from datetime import datetime
from common_classes.loggable import Loggable
from sec_communicator_api import SecCommunicatorApi
from sys import getsizeof

class WorkerApi(Loggable):
  """
  backend_tasks - BackendTasksApi
  sec_communicator - SecCommunicatorApi
  """
  def __init__(self):
    super().__init__("WorkerApi")
    self._backend_tasks = BackendTasksApi()
    self._sec_communicator = SecCommunicatorApi()

  def getCompanyAcronymForGathering(self):
    self._debug("getCompanyAcronymForGathering", "Start")
    result = self._backend_tasks.getAcronymOfTaskWithProgressInitiated()
    self._debug("getCompanyAcronymForGathering", "Finish - result: %s\n" % result)
    return result

  def getDataFromSec(self, acronym):
    self._debug("getDataFromSec", "Start - acronym: %s" % acronym)
    result = {}

    self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining company id")
    company_id = self._sec_communicator.getCompanyIdWithAcronym(acronym)

    if company_id:
      self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining 10-K filings")
      html_document_with_10k_search_results = self._sec_communicator.get10kSearchResultsWithCompanyId(
        company_id
      )

    if html_document_with_10k_search_results:
      self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining 10-K accession_numbers")
      accession_numbers = self._sec_communicator.get10kAccNoFromHtmlDocument(
        html_document_with_10k_search_results
      )

    if accession_numbers:
      self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining 10-K financial statements ids")
      pivot_date = datetime.strptime("2015-01-01", '%Y-%m-%d')
      for date_str, accession_number in accession_numbers.items():
        next_date = datetime.strptime(date_str, '%Y-%m-%d')
        if next_date < pivot_date:
          continue
        html_document_with_10k_report = self._sec_communicator.get10KReportWithCikAndAccNo(
          company_id,
          accession_number
        )
        if html_document_with_10k_report:
          income_statements_ids = self._sec_communicator.getIncomeStatementsIdsFromHtmlDocument(
            html_document_with_10k_report
          )
          result[date_str] = {
            "data": dict(),
            "currency_units": None
          }
          for income_statement_id in income_statements_ids:
            self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining data from financial statement")
            html_document_with_financial_statement = self._sec_communicator.getFinancialStatementDocument(
              company_id,
              accession_number,
              income_statement_id
            )
            if html_document_with_financial_statement:
              financial_data = self._sec_communicator.getFinancialStatementWithHtmlDocument(
                html_document_with_financial_statement
              )
              result[date_str]["data"] = result[date_str]["data"] | financial_data[0]
              result[date_str]["currency_units"] = financial_data[1]

    self._debug("getDataFromSec", "Finish - result: %s \n" % result)
    return result
