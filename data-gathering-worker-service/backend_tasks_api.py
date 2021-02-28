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


  def updateTaskByCompanyAcronym(self, company_acronym, progress):
    self._debug("updateTaskByCompanyAcronym", "Start - company_acronym: %s, progress: %s" % (company_acronym, progress))

    task = self.getTaskByCompanyAcronym(company_acronym)
    task["progress"] = progress

    relative_location = self._getRelativeLocation(company_acronym)
    with open(relative_location, "w") as write_file:
        dump(task, write_file)
    result = "task has been updated"

    self._debug("updateTaskByCompanyAcronym", "Finish - result: %s" % result)
    return result

  def getAcronymOfTaskWithProgressInitiated(self):
    self._debug("getAcronymOfTaskWithProgressInitiated", "Start")
    result = None

    directory = self._getRelativeLocationOfBackendTasks()
    for filename in listdir(directory):
      if filename.endswith(".json"):
        task = self.getTaskByCompanyAcronym(filename.replace(".json", ""))
        if task["progress"] == "task initiated":
          result = task["acronym"]
          break

    self._debug("getAcronymOfTaskWithProgressInitiated", "Finish - result: %s" % result)
    return result

  def getTaskByCompanyAcronym(self, company_acronym):
    self._debug("getTaskByCompanyAcronym", "Start - company_acronym: %s" % company_acronym)
    result = None

    relative_location = self._getRelativeLocation(company_acronym)
    if path.exists(relative_location):
      with open(relative_location, "r") as read_file:
        result = load(read_file)

    self._debug("getTaskByCompanyAcronym", "Finish - result: %s" % result)
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

