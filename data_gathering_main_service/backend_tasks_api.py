import json
from os import path

from common.loggable_api import Loggable
from common.backend_task_progress import BackendTaskProgress

class BackendTasks(Loggable):
  """
  CRUDs the backend_tasks directly through the file system.
  TODO: implement direct communication with an in-memory database, i.e. Redis, and remove any file system use in v1.0
  """
  def __init__(self, log_id):
    """
    Keyword arguments:
      log_id -- str.
    """
    super().__init__(log_id, "BackendTasksApi")

  def createTaskByCompanyAcronym(self, acronym):
    """
    Keyword arguments:
      acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("createTaskByCompanyAcronym", "Start - acronym: %s" % acronym)
    task = {
      "acronym": acronym,
      "progress": BackendTaskProgress.STARTED.value
    }
    backend_task_path = self._getBackendTaskPath(acronym)
    with open(backend_task_path, "w+") as write_file:
        json.dump(task, write_file)
    self._debug("createTaskByCompanyAcronym","Finish")

  def getTaskByCompanyAcronym(self, acronym):
    """
    Returns a dict with the information about a backend task.
    Keyword arguments:
      acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("getTaskByCompanyAcronym", "Start - acronym: %s" % acronym)
    result = dict()
    backend_task_path = self._getBackendTaskPath(acronym)
    if path.exists(backend_task_path):
      with open(backend_task_path, "r") as read_file:
        result = json.load(read_file)
    self._debug("getTaskByCompanyAcronym", "Finish - result: %s" % result)
    return result

  def _getBackendTaskPath(self, company_acronym):
    """
    TODO: remove in v1.0.
    Returns the path to the file with the backend_task in the file-system.
    Keyword arguments:
      acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    print(path.dirname(__file__))
    return path.join(
      path.dirname(__file__),
      "..",
      "common",
      "backend_tasks_db",
      "data_gathering",
      "%s.json" % company_acronym
    )