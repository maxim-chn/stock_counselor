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


  def createTaskByCompanyAcronym(self, company_acronym, progress):
    self._debug(
      "createTaskByCompanyAcronym",
      "Start - company_acronym: %s, progress: %s" % (company_acronym, progress)
    )
    task = {"acronym": company_acronym, "progress": progress}
    relative_location = self._getRelativeLocation(company_acronym)
    with open(relative_location, "w") as write_file:
        json.dump(task, write_file)
    result = "task has been created"

    self._debug("createTaskByCompanyAcronym","Finish - result: %s" % (result))
    return result

  def getTaskByCompanyAcronym(self, company_acronym):
    self._debug("getTaskByCompanyAcronym", "Start - company_acronym: %s" % (company_acronym))
    result = None

    relative_location = self._getRelativeLocation(company_acronym)
    if path.exists(relative_location):
      with open(relative_location, "r") as read_file:
        result = json.load(read_file)

    self._debug("getTaskByCompanyAcronym", "Start - result: %s" % (result))
    return result

  def _getRelativeLocation(self, company_acronym):
    return path.join(
      path.dirname(__file__),
      "backend_tasks",
      "remove_in_alpha",
      '%s.json' % (company_acronym)
    )