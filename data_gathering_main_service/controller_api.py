from common.data_gathering_backend_tasks_api import BackendTasks
from common.loggable_api import Loggable
from common.data_gathering.backend_tasks.task import Progress
class Controller(Loggable):
  """
  This is our Controller Logic which reveals an API for the Boundary.
  The available methods connect between an input from the Boundary and the backend tasks.
  """

  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Keyword arguments:
      service_name -- str.
    """
    super().__init__(service_name, "Controller")
    self._backend_tasks = BackendTasks(service_name)

  def collectFinancialDataFor(self, company_acronym):
    """
    Returns str.
    It represents the backend task progress for a collection of a company's financial data.
    Keyword arguments:
      company_acronym -- str -- unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("collectFinancialDataFor", "Start\ncompany_acronym:\t%s" % company_acronym)
    result = Progress.NOT_EXPECTED.value
    progress = None
    
    try:
      progress = self._collectionProgressFor(company_acronym)
    except RuntimeError as err:
      err_msg = "Failed at retrieving financial data collection progress\n%s" % str(err)
      self._error("collectFinancialDataFor", err_msg)
      return result
    
    if progress == Progress.NOT_STARTED:
      try:
        task = self._backend_tasks.createTaskBy(company_acronym)
        result = task.progress.value
      except RuntimeError as err:
        err_msg = "Failed at creating a new backend task for financial data collection\n%s" % str(err)
        self._error("collectFinancialDataFor", err_msg)
        return result
    else:
      result = progress.value
    
    self._debug("collectFinancialDataFor", "Finish\nresult:\t%s\n" % result)
    return result

  def _collectionProgressFor(self, company_acronym):
    """
    Returns Progress.
    Raises RuntimeError.
    Keyword arguments:
      company_acronym -- str -- unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("_collectionProgressFor", "Start\ncompany_acronym:\t%s" % company_acronym)
    
    try:
      task = self._backend_tasks.getTaskBy(company_acronym)
      if not task:
        result = Progress.NOT_STARTED
      else:
        result = task.progress
    except RuntimeError as err:
      raise RuntimeError("%s -- _collectionProgressFor -- Failed\n%s" % (self._class_name, str(err)))
    
    self._debug("_collectionProgress", "Finish\nresult:\t%s" % result)
    return result