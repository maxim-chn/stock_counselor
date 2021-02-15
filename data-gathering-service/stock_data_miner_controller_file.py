"""
Operates the CentralState object

"""
from backend_tasks_file import BackendTasks
import logging
from stock_data_miner_controller.datum import Datum
from stock_data_miner_controller.central_state import CentralState

class StockDataMinerController:
  """
  backend_tasks - BackendTasks
  """
  def __init__(self):
    self._backend_tasks = BackendTasks()

  def collectStockData(self, company_acronym):
    msg = '%s - %s() - Start - company_acronym: %s' % (
      "StockDataMinerController",
      "collectStockData",
      company_acronym
    )
    logging.getLogger('stock_data_miner').debug(msg)

    if self.isCollectionInProgress(company_acronym):
      result = "Collection is Already in Progress"
    else:
      self.createNewCollectionTask(company_acronym)
      result = "Stock Data Collection has been Started"

    msg = '%s - %s() - Finish - result: %s' % (
      "StockDataMinerController",
      "collectStockData",
      result
    )
    logging.getLogger('stock_data_miner').debug(msg)

    return result

  def createNewCollectionTask(self, company_acronym):
    msg = '%s - %s() - Start - company_acronym: %s' % (
      "StockDataMinerController",
      "createNewCollectionTask",
      company_acronym
    )
    logging.getLogger('stock_data_miner').debug(msg)

    result = self._backend_tasks.createTaskByCompanyAcronym(company_acronym, "task initiated")

    msg = '%s - %s() - Finish - result: %s' % (
      "StockDataMinerController",
      "createNewCollectionTask",
      result
    )
    logging.getLogger('stock_data_miner').debug(msg)

    return result

  def isCollectionInProgress(self, company_acronym):
    msg = '%s - %s() - Start - company_acronym: %s' % (
      "StockDataMinerController",
      "isCollectionInProgress",
      company_acronym
    )
    logging.getLogger('stock_data_miner').debug(msg)

    background_task = self._backend_tasks.getTaskByCompanyAcronym(company_acronym)

    result = background_task is not None

    msg = '%s - %s() - Finish - result: %r' % (
      "StockDataMinerController",
      "isCollectionInProgress",
      result
    )
    logging.getLogger('stock_data_miner').debug(msg)

    return result

  def passCompanyAcronymToCentralState(self, company_acronym):
    input = Datum("Company Acronym", company_acronym)
    state_machine = CentralState(input)
    response = state_machine.executeFlow()
    return response



