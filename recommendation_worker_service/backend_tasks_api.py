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

  def updateTaskByUserId(self, user_id, progress):
    """
    Returns BackendTaskProgress.
    It represents if the task progress update has succeeded.
    Keyword arguments:
      progress -- str -- represents the task's progress.
      user_id -- str -- unique identifier of a user inside our program.
    """
    self._debug("updateTaskByUserId", "Start - user_id: %s, progress: %s" % (user_id, progress))
    result = BackendTaskProgress.FAILED_TO_UPDATE_PROGRESS
    task = self.getTaskByUserId(user_id)
    if task:
      task["progress"] = progress
      backend_task_path = self._getBackendTaskPath(user_id)
      with open(backend_task_path, "w") as write_file:
        dump(task, write_file)
      result = BackendTaskProgress.UPDATED_PROGRESS
    self._debug("updateTaskByUserId", "Finish - result: %s" % result.value)
    return result

  def getUserIdFromNewTask(self):
    """
    Returns a str or None.
    The str is a user_id.
    """
    self._debug("getUserIdFromNewTask", "Start")
    result = None
    be_tasks_directory = self._getBackendTasksPath()
    for filename in listdir(be_tasks_directory):
      if filename.endswith(".json"):
        task = self.getTaskByUserId(filename.replace(".json", ""))
        if "progress" in task.keys():
          if task["progress"] == BackendTaskProgress.STARTED.value:
            result = task["user_id"]
            break
    self._debug("getUserIdFromNewTask", "Finish - result: %s" % result)
    return result

  def getTaskByUserId(self, user_id):
    """
    Returns a dict.
    It represents the backend task for calculating investment recommendation for a user.
    Keyword arguments:
      user_id -- str -- unique identifier of a user inside our program.
    """
    self._debug("getTaskByUserId", "Start - user_id: %s" % user_id)
    result = dict()
    backend_task_path = self._getBackendTaskPath(user_id)
    if path.exists(backend_task_path):
      with open(backend_task_path, "r") as read_file:
        result = load(read_file)
    self._debug("getTaskByUserId", "Finish - result: %s" % result)
    return result

  def _getBackendTaskPath(self, user_id):
    """
    TODO: remove in v1.0.
    Returns a path.
    It is the location of the file with the backend_task in the file-system.
    Keyword arguments:
      user_id -- str -- an unique identifier of a user inside our program.
    """
    return path.join(
      path.dirname(__file__),
      "..",
      "common",
      "backend_tasks_db",
      "recommendation_tasks_db",
      "%s.json" % user_id
    )

  def _getBackendTasksPath(self):
    """
    TODO: remove in v1.0.
    Returns a path.
    It is the location to the directory with the backend tasks related to the investment recommendation calculation.
    """
    return path.join(
      path.dirname(__file__),
      "..",
      "common",
      "backend_tasks_db",
      "recommendation_tasks_db"
    )

