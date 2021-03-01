"""
This is our Controller logic.
It reveals an internal API with the methods that map the request to gather data about a company
to a backend task.
The backend task will later be picked up by an external worker service.
"""

from backend_tasks_api import BackendTasksApi
from common_classes.loggable import Loggable

class StockDataMinerControllerApi(Loggable):
    """
    backend_tasks - BackendTasksApi
    """
    def __init__(self):
      super().__init__("StockDataMinerControllerApi")
      self._backend_tasks = BackendTasksApi()
      

    def collectStockData(self, company_acronym):
      self._debug("collectStockData", "Start - company_acronym: %s" % company_acronym)
      result = None

      if self.isCollectionInProgress(company_acronym):
        result = "Collection is Already in Progress"
      else:
        self.createNewCollectionTask(company_acronym)
        result = "Stock Data Collection has been Started"

      self._debug("collectStockData", "Finish - result: %s\n" % result)
      return result

    def createNewCollectionTask(self, company_acronym):
      self._debug("createNewCollectionTask", "Start - company_acronym: %s" % company_acronym)
      result = self._backend_tasks.createTaskByCompanyAcronym(company_acronym, "task initiated")

      self._debug("createNewCollectionTask", "Result - result: %s" % result)
      return result

    def isCollectionInProgress(self, company_acronym):
      self._debug("isCollectionInProgress", "Start - company_acronym: %s" % company_acronym)
      background_task = self._backend_tasks.getTaskByCompanyAcronym(company_acronym)
      result = background_task is not None

      self._debug("isCollectionInProgress", "Finish - result: %s" % result)
      return result