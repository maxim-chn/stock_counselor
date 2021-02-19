"""
Communicates with an in-memory database that manages the backend tasks.
"""

from json import dump, load
from logging import getLogger
from os import listdir, path


class BackendTasksApi:
  """
  database_connection - dictionary
  """

  def __init__(self, database_connection=dict()):
    # TODO: connect to module that communicates with RAM
    # TODO: implement singleton
    self._database_connection = database_connection


  def updateTaskByCompanyAcronym(self, company_acronym, progress):
    msg = '%s - %s() - Start - company_acronym: %s, progress: %s' % (
      "BackendTasksApi",
      "updateTaskByCompanyAcronym",
      company_acronym,
      progress
    )
    getLogger('data-gathering-worker-service').debug(msg)

    task = self.getTaskByCompanyAcronym(company_acronym)
    task["progress"] = progress

    relative_location = self._getRelativeLocation(company_acronym)
    with open(relative_location, "w") as write_file:
        dump(task, write_file)
    result = "task has been updated"

    msg = '%s - %s() - Finish - result: %s' % (
      "BackendTasksApi",
      "updateTaskByCompanyAcronym",
      result
    )
    getLogger('data-gathering-worker-service').debug(msg)

    return result

  def getAcronymOfTaskWithProgressInitiated(self):
    msg = '%s - %s() - Start' % (
      "BackendTasksApi",
      "getAcronymOfTaskWithProgressInitiated"
    )
    getLogger('data-gathering-worker-service').debug(msg)

    result = None
    directory = self._getRelativeLocationOfBackendTasks()
    for filename in listdir(directory):
      if filename.endswith(".json"):
        task = self.getTaskByCompanyAcronym(filename.replace(".json", ""))
        if task["progress"] == "task initiated":
          result = task["acronym"]
          break

    msg = '%s - %s() - Finish - result: %s' % (
      "BackendTasksApi",
      "getAcronymOfTaskWithProgressInitiated",
      result
    )
    getLogger('data-gathering-worker-service').debug(msg)

    return result


  def getTaskByCompanyAcronym(self, company_acronym):
    msg = '%s - %s() - Start - company_acronym: %s' % (
      "BackendTasksApi",
      "getTaskByCompanyAcronym",
      company_acronym
    )
    getLogger('data-gathering-worker-service').debug(msg)

    relative_location = self._getRelativeLocation(company_acronym)
    result = None
    if path.exists(relative_location):
      with open(relative_location, "r") as read_file:
        result = load(read_file)

    msg = '%s - %s() - Finish - result: %s' % (
      "BackendTasksApi",
      "getTaskByCompanyAcronym",
      result
    )
    getLogger('data-gathering-worker-service').debug(msg)

    return result

  def _getRelativeLocation(self, company_acronym):
    return path.join(
      path.dirname( __file__ ),
      "..",
      "data-gathering-main-service",
      "backend_tasks",
      "remove_in_alpha",
      '%s.json' % (company_acronym)
    )

  def _getRelativeLocationOfBackendTasks(self):
    return path.join(
      path.dirname( __file__ ),
      "..",
      "data-gathering-main-service",
      "backend_tasks",
      "remove_in_alpha"
    )

