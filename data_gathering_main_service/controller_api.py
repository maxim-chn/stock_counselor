from data_gathering_main_service.backend_tasks_api import BackendTasks
from common.backend_task_progress import BackendTaskProgress
from common.loggable_api import Loggable
from enum import Enum

class CollectionProgress(Enum):
  """
  Represents the State of the Financial Data Collection Task
  """
  STARTED = "Financial Data Collection has been Started"
  IN_PROGRESS = "Financial Data Collection is in Progress"
  FINISHED = "Financial Data has been Collected"

class Controller(Loggable):
  """
  This is our Controller Logic which reveals an API for the Boundary.
  The available methods connect between an input from the Boundary and the backend tasks.
  """

  def __init__(self, log_id):
    """
    Keyword arguments:
      log_id -- str.
    """
    super().__init__(log_id, "Controller")
    self._backend_tasks = BackendTasks(log_id)

  def collectFinancialData(self, company_acronym):
    """
    Returns a str. It represents the backend task progress for a collection of financial data about a certain
    company.
    Keyword arguments:
      acronym -- str -- unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("collectFinancialData", "Start - company_acronym: %s" % company_acronym)
    progress = self._collectionProgress(company_acronym)
    if not progress:
      self._backend_tasks.createTaskByCompanyAcronym(company_acronym)
      result = CollectionProgress.STARTED.value
    elif progress == BackendTaskProgress.FINISHED.value:
      result = CollectionProgress.FINISHED.value
    else:
      result = CollectionProgress.IN_PROGRESS.value
    self._debug("collectFinancialData", "Finish - result: %s\n" % result)
    return result

  def _collectionProgress(self, company_acronym):
    """
    Returns a str. It is a value of the BackendTaskProgress Enum.
    Keyword arguments:
      acronym -- str -- unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("_collectionProgress", "Start - company_acronym: %s" % company_acronym)
    background_task = self._backend_tasks.getTaskByCompanyAcronym(company_acronym)
    if not "progress" in background_task.keys():
      result = None
    else:
      result = background_task["progress"]
    self._debug("_collectionProgress", "Finish - result: %s" % result)
    return result