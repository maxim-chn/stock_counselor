"""
Communicates with an in-memory database that manages the backend tasks.
"""

import json
from os import path

from common_classes.loggable import Loggable

class BackendTasksApi(Loggable):
  """
  database_connection - dictionary
  """
  def __init__(self, database_connection=dict()):
    # TODO: connect to module that communicates with RAM
    super().__init__("BackendTasksApi")
    self._database_connection = database_connection


  def createTaskByUserId(self, user_id, progress):
    self._debug(
      "createTaskByUserId",
      "Start - user_id: %s, progress: %s" % (user_id, progress)
    )
    task = {"user_id": user_id, "progress": progress}
    relative_location = self._getRelativeLocation(user_id)
    with open(relative_location, "w") as write_file:
        json.dump(task, write_file)
    result = "task has been created"

    self._debug("createTaskByUserId", "Finish - result: %s" % result)
    return result

  def getTaskByUserId(self, user_id):
    self._debug("getTaskByUserId", "Start - user_id: %s" % user_id)
    result = None

    relative_location = self._getRelativeLocation(user_id)
    if path.exists(relative_location):
      with open(relative_location, "r") as read_file:
        result = json.load(read_file)

    self._debug("getTaskByUserId", "Start - result: %s" % result)
    return result

  def _getRelativeLocation(self, user_id):
    return path.join(
      path.dirname(__file__),
      "backend_tasks",
      "remove_in_alpha",
      '%s.json' % user_id
    )