from common.backend_task_progress import BackendTaskProgress
from common.loggable_api import Loggable
from json import dump, load
from os import listdir, path

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
    super().__init__(log_id, "BackendTasks")

  def getCompanyAcronymFromNewTask(self):
    """
    Returns a str that contains company acronym (symbol at a stock exchange) in case there is a new backend task.
    Returns None, otherwise.
    """
    self._debug("getCompanyAcronymFromNewTask", "Start")
    result = None
    be_tasks_directory = self._getBackendTasksPath()
    for filename in listdir(be_tasks_directory):
      if filename.endswith(".json"):
        task = self.getTaskByCompanyAcronym(filename.replace(".json", ""))
        if task["progress"] == BackendTaskProgress.STARTED.value:
          result = task["acronym"]
          break
    self._debug("getCompanyAcronymFromNewTask", "Finish - result: %s" % result)
    return result

  def getTaskByCompanyAcronym(self, acronym):
    """
    Returns a dict that represents a backend task.
    Returns None in case the task is not found.
    Keyword arguments:
      acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("getTaskByCompanyAcronym", "Start - acronym: %s" % acronym)
    result = None
    backend_task_path = self._getBackendTaskPath(acronym)
    if path.exists(backend_task_path):
      with open(backend_task_path, "r") as read_file:
        result = load(read_file)
    self._debug("getTaskByCompanyAcronym", "Finish - result: %s" % result)
    return result

  def updateTaskByCompanyAcronym(self, acronym, progress):
    """
    Returns BackendTaskProgress. It represents whether the task progress update has succeeded.
    Keyword arguments:
      acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
      progress -- str -- represents the task's progress.
    """
    self._debug("updateTaskByCompanyAcronym", "Start - acronym: %s, progress: %s" % (acronym, progress))
    result = BackendTaskProgress.FAILED_TO_UPDATE_PROGRESS
    task = self.getTaskByCompanyAcronym(acronym)
    if task:
      task["progress"] = progress
      backend_task_path = self._getBackendTaskPath(acronym)
      with open(backend_task_path, "w") as write_file:
          dump(task, write_file)
      result = BackendTaskProgress.UPDATED_PROGRESS
    self._debug("updateTaskByCompanyAcronym", "Finish - result: %s" % result.value)
    return result

  def _getBackendTaskPath(self, company_acronym):
    """
    TODO: remove in v1.0.
    Returns the path to the file with the backend_task in the file-system.
    Keyword arguments:
      company_acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    return path.join(
      path.dirname(__file__),
      "..",
      "common",
      "backend_tasks_db",
      "data_gathering",
      "%s.json" % company_acronym
    )

  def _getBackendTasksPath(self):
    """
    TODO: remove in v1.0.
    Returns the path to the directory with the backend tasks related to the financial data gathering.
    """
    return path.join(
      path.dirname( __file__ ),
      "..",
      "common",
      "backend_tasks_db",
      "data_gathering"
    )
