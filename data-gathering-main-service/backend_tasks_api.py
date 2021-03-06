import json
from os import path

from common_classes.loggable import Loggable

class BackendTasksApi(Loggable):
  """
  Communicates with an in-memory database that manages the backend tasks.
  """
  def __init__(self, database_connection=dict()):
    # TODO: connect to a module that communicates with RAM, i.e. RabbitMQ
    super().__init__("BackendTasksApi")
    self._database_connection = database_connection

  def createTaskByCompanyAcronym(self, company_acronym, progress):
    """
    Keyword arguments:
      company_acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
      progress -- str -- task progress status, i.e. "task initiated"
    """
    self._debug(
      "createTaskByCompanyAcronym",
      "Start - company_acronym: %s, progress: %s" % (company_acronym, progress)
    )
    task = {
      "acronym": company_acronym,
      "progress": progress
    }
    relative_location = self._getLocationOfBackendTasks(company_acronym)
    with open(relative_location, "w") as write_file:
        json.dump(task, write_file)
    self._debug("createTaskByCompanyAcronym","Finish - task has been created")

  def getTaskByCompanyAcronym(self, company_acronym):
    """
    Returns a dict with the information about a backend task.
    """
    self._debug("getTaskByCompanyAcronym", "Start - company_acronym: %s" % company_acronym)
    result = None

    relative_location = self._getLocationOfBackendTasks(company_acronym)
    if path.exists(relative_location):
      with open(relative_location, "r") as read_file:
        result = json.load(read_file)

    self._debug("getTaskByCompanyAcronym", "Start - result: %s" % result)
    return result

  def _getLocationOfBackendTasks(self, company_acronym):
    """
    TODO: remove in Alpha.
    Returns the location of a directory where we store our backend tasks files.
    """
    return path.join(
      path.dirname(__file__),
      "backend_tasks",
      "remove_in_alpha",
      '%s.json' % (company_acronym)
    )