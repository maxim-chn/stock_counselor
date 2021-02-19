"""
This is our Controller logic.
It reveals an internal API with the methods that map the request to gather data about a company
to a backend task.
The backend task will later be picked up by an external worker service.
"""

from backend_tasks_api import BackendTasksApi
import logging

class StockDataMinerControllerApi:
    """
    backend_tasks - BackendTasksApi
    """
    def __init__(self):
      self._backend_tasks = BackendTasksApi()
      

    def collectStockData(self, company_acronym):
      msg = '%s - %s() - Start - company_acronym: %s' % (
        "StockDataMinerControllerApi",
        "collectStockData",
        company_acronym
      )
      logging.getLogger('data-gathering-main-service').debug(msg)

      result = None

      if self.isCollectionInProgress(company_acronym):
        result = "Collection is Already in Progress"
      else:
        self.createNewCollectionTask(company_acronym)
        result = "Stock Data Collection has been Started"

      msg = '%s - %s() - Finish - result: %s' % (
        "StockDataMinerControllerApi",
        "collectStockData",
        result
      )
      logging.getLogger('data-gathering-main-service').debug(msg)

      return result

    def createNewCollectionTask(self, company_acronym):
      msg = '%s - %s() - Start - company_acronym: %s' % (
        "StockDataMinerControllerApi",
        "createNewCollectionTask",
        company_acronym
      )
      logging.getLogger('data-gathering-main-service').debug(msg)

      result = self._backend_tasks.createTaskByCompanyAcronym(company_acronym, "task initiated")

      msg = '%s - %s() - Finish - result: %s' % (
        "StockDataMinerControllerApi",
        "createNewCollectionTask",
        result
      )
      logging.getLogger('data-gathering-main-service').debug(msg)

      return result

    def isCollectionInProgress(self, company_acronym):
      msg = '%s - %s() - Start - company_acronym: %s' % (
        "StockDataMinerControllerApi",
        "isCollectionInProgress",
        company_acronym
      )
      logging.getLogger('data-gathering-main-service').debug(msg)

      background_task = self._backend_tasks.getTaskByCompanyAcronym(company_acronym)

      result = background_task is not None

      msg = '%s - %s() - Finish - result: %r' % (
        "StockDataMinerControllerApi",
        "isCollectionInProgress",
        result
      )
      logging.getLogger('data-gathering-main-service').debug(msg)

      return result