from json import dump, load
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
    super().__init__(log_id, "BackendTasks")

  def createTaskByUserId(self, user_id):
    """
    Keyword arguments:
      user_id -- str -- an unique identifier of a user inside our program.
    """
    self._debug("createTaskByUserId", "Start - user_id: %s" % user_id)
    task = {
      "user_id": user_id,
      "progress": BackendTaskProgress.STARTED.value
    }
    backend_task_path = self._getBackendTaskPath(user_id)
    with open(backend_task_path, "w+") as write_file:
      dump(task, write_file)
    self._debug("createTaskByUserId", "Finish")

  def getTaskByUserId(self, user_id):
    """
    Returns a dict with the information about a backend task.
    Keyword arguments:
      user_id -- str -- an unique identifier of a user inside our program.
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
    TODO: remove in v1.0
    Returns a path to the backend task.
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