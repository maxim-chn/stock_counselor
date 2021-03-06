from json import dump, load
from common_classes.loggable import Loggable
from os import listdir, path

class BackendTasksApi(Loggable):
  """
  Communicates with an in-memory database that manages the backend tasks.
  """

  def __init__(self, database_connection=dict()):
    # TODO: connect to module that communicates with RAM, i.e. RabbitMQ
    super().__init__("BackendTasksApi")
    self._database_connection = database_connection

  def getAcronymOfTaskWithProgressInitiated(self):
    """
    Returns a str with the company acronym from a task with the progress "task initiated" which represents
    the new backend task.
    Returns None in case there is no new backend task.
    """
    self._debug("getAcronymOfTaskWithProgressInitiated", "Start")
    result = None

    directory = self._getLocationOfBackendTasks()
    for filename in listdir(directory):
      if filename.endswith(".json"):
        task = self.getTaskByCompanyAcronym(filename.replace(".json", ""))
        if task["progress"] == "task initiated":
          result = task["acronym"]
          break

    self._debug("getAcronymOfTaskWithProgressInitiated", "Finish - result: %s" % result)
    return result

  def getTaskByCompanyAcronym(self, company_acronym):
    """
    Returns a dict that represents a backend task.
    Returns None in case the task is not found.

    Keyword arguments:
      company_acronym -- str -- unique id of a company at a stock exchange, i.e.e NASDAQ.
    """
    self._debug("getTaskByCompanyAcronym", "Start - company_acronym: %s" % company_acronym)
    result = None

    relative_location = self._getLocationOfABackendTaskBy(company_acronym)
    if path.exists(relative_location):
      with open(relative_location, "r") as read_file:
        result = load(read_file)

    self._debug("getTaskByCompanyAcronym", "Finish - result: %s" % result)
    return result

  def updateTaskByCompanyAcronym(self, company_acronym, progress):
    """
    Keyword arguments:
      company_acronym -- str -- unique id of a company at a stock exchange, i.e.e NASDAQ.
      progress -- str -- represents the task's progress.
    """
    self._debug("updateTaskByCompanyAcronym", "Start - company_acronym: %s, progress: %s" % (company_acronym, progress))

    task = self.getTaskByCompanyAcronym(company_acronym)
    task["progress"] = progress

    relative_location = self._getLocationOfABackendTaskBy(company_acronym)
    with open(relative_location, "w") as write_file:
        dump(task, write_file)
    result = "task has been updated"

    self._debug("updateTaskByCompanyAcronym", "Finish - result: %s" % result)
    return result

  def _getLocationOfABackendTaskBy(self, company_acronym):
    """
    TODO: remove in Alpha.
    Returns the location of a file that represents the backend task for a certain company.

    Keyword arguments:
      company_acronym -- str -- unique id of a company at a stock exchange, i.e.e NASDAQ.
    """
    return path.join(
      path.dirname( __file__ ),
      "..",
      "data-gathering-main-service",
      "backend_tasks",
      "remove_in_alpha",
      '%s.json' % (company_acronym)
    )

  def _getLocationOfBackendTasks(self):
    """
    TODO: remove in Alpha.
    Returns the location of a directory where we store our backend tasks files.
    """
    return path.join(
      path.dirname( __file__ ),
      "..",
      "data-gathering-main-service",
      "backend_tasks",
      "remove_in_alpha"
    )

