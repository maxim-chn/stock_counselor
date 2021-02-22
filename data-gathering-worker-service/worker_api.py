"""
It reveals an internal API for executing the backend tasks related to company data gathering
"""

from backend_tasks_api import BackendTasksApi
from logging import getLogger
from sec_communicator_api import SecCommunicatorApi

class WorkerApi:

  """
  backend_tasks - BackendTasksApi
  sec_communicator - SecCommunicatorApi
  """
  def __init__(self):
    self._backend_tasks = BackendTasksApi()
    self._sec_communicator = SecCommunicatorApi()

  def getCompanyAcronymForGathering(self):
    msg = '\n%s - %s() - Start' % (
      "WorkerApi",
      "getCompanyAcronymForGathering"
    )
    getLogger('data-gathering-worker-service').debug(msg)

    result = self._backend_tasks.getAcronymOfTaskWithProgressInitiated()

    msg = '%s - %s() - Finish - result: %s\n' % (
      "WorkerApi",
      "getCompanyAcronymForGathering",
      result
    )
    getLogger('data-gathering-worker-service').debug(msg)

    return result

  def getDataFromSec(self, acronym):
    msg = '\n%s - %s() - Start - acronym: %s' % (
      "WorkerApi",
      "getDataFromSec",
      acronym
    )
    getLogger('data-gathering-worker-service').debug(msg)

    result = None

    self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining company id")
    company_id = self._sec_communicator.getCompanyIdWithAcronym(acronym)
    html_document_with_10k_search_results = None
    accesion_numbers = None

    if company_id:
      self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining 10-K filings")
      html_document_with_10k_search_results = self._sec_communicator.get10kSearchResultsWithCompanyId(
        company_id
      )

    if html_document_with_10k_search_results:
      accesion_numbers = self._sec_communicator.get10kAccNoFromHtmlDocument(
        html_document_with_10k_search_results
      )

    msg = '%s - %s() - Finish - result: %s\n' % (
      "WorkerApi",
      "getDataFromSec",
      result
    )
    getLogger('data-gathering-worker-service').debug(msg)

    return result


