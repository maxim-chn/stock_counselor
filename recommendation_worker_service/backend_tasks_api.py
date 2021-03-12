"""
Communicates with an in-memory database that manages the backend tasks.
"""

from json import dump, load
from common_classes.loggable import Loggable
from os import listdir, path

class BackendTasksApi(Loggable):
  """
  database_connection - dictionary
  """
  def __init__(self, database_connection=dict()):
    # TODO: connect to module that communicates with RAM
    # TODO: implement singleton
    super().__init__("BackendTasksApi")
    self._database_connection = database_connection


  def updateTaskByUserId(self, user_id, progress):
    self._debug("updateTaskByUserId", "Start - company_acronym: %s, progress: %s" % (user_id, progress))

    task = self.getTaskByUserId(user_id)
    task["progress"] = progress

    relative_location = self._getRelativeLocation(user_id)
    with open(relative_location, "w") as write_file:
        dump(task, write_file)
    result = "task has been updated"

    self._debug("updateTaskByUserId", "Finish - result: %s" % result)
    return result

  def getUserIdOfTaskWithProgressInitiated(self):
    self._debug("getUserIdOfTaskWithProgressInitiated", "Start")
    result = None

    directory = self._getRelativeLocationOfBackendTasks()
    for filename in listdir(directory):
      if filename.endswith(".json"):
        task = self.getTaskByUserId(filename.replace(".json", ""))
        if task["progress"] == "task initiated":
          result = task["user_id"]
          break

    self._debug("getUserIdOfTaskWithProgressInitiated", "Finish - result: %s" % result)
    return result

  def getTaskByUserId(self, user_id):
    self._debug("getTaskByUserId", "Start - company_acronym: %s" % user_id)
    result = None

    relative_location = self._getRelativeLocation(user_id)
    if path.exists(relative_location):
      with open(relative_location, "r") as read_file:
        result = load(read_file)

    self._debug("getTaskByUserId", "Finish - result: %s" % result)
    return result

  def _getRelativeLocation(self, user_id):
    return path.join(
      path.dirname(__file__),
      "..",
      "recommendation_main_service",
      "backend_tasks",
      "remove_in_alpha",
      '%s.json' % user_id
    )

  def _getRelativeLocationOfBackendTasks(self):
    return path.join(
      path.dirname(__file__),
      "..",
      "recommendation_main_service",
      "backend_tasks",
      "remove_in_alpha"
    )

