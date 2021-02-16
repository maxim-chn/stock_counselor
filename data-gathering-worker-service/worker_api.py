
from backend_tasks_api import BackendTasksApi
from logging import getLogger

class WorkerApi:

  def __init__(self):
    self._backend_tasks = BackendTasksApi()


  def getCompanyAcronymForGathering(self):
    msg = '%s - %s() - Start' % (
      "WorkerApi",
      "getCompanyAcronymForGathering"
    )
    getLogger('data-gathering-worker-service').debug(msg)

    result = self._backend_tasks.getAcronymOfTaskWithProgressInitiated()

    msg = '%s - %s() - Finish - result: %s' % (
      "WorkerApi",
      "getCompanyAcronymForGathering",
      result
    )
    getLogger('data-gathering-worker-service').debug(msg)

    return result

  def getDataFromSec(self, acronym):
    msg = '%s - %s() - Start - acronym: %s' % (
      "WorkerApi",
      "getDataFromSec",
      acronym
    )
    getLogger('data-gathering-worker-service').debug(msg)

    result = None

    self._backend_tasks.updateTaskByCompanyAcronym(acronym, "obtaining company id")

    msg = '%s - %s() - Finish - result: %s' % (
      "WorkerApi",
      "getDataFromSec",
      result
    )
    getLogger('data-gathering-worker-service').debug(msg)

    return result