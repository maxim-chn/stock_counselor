"""
This is our Controller logic.
It reveals an internal API with the methods that map the request to gather data about a company
to a backend task.
The backend task will later be picked up by an external worker service.
"""

from backend_tasks_api import BackendTasksApi
from common_classes.loggable import Loggable

class RecommendationControllerApi(Loggable):
    """
    backend_tasks - BackendTasksApi
    """
    def __init__(self):
      super().__init__("RecommendationControllerApi")
      self._backend_tasks = BackendTasksApi()
      

    def calculateRecommendation(self, user_id):
      self._debug("calculateRecommendation", "Start - user_id: %s" % user_id)
      result = None

      if self.isCalculationInProgress(user_id):
        result = "Calculation is Already in Progress"
      else:
        self.createNewCalculationTask(user_id)
        result = "Calculation has been Started"

      self._debug("calculateRecommendation", "Finish - result: %s\n" % result)
      return result

    def createNewCalculationTask(self, user_id):
      self._debug("createNewCalculationTask", "Start - user_id: %s" % user_id)
      result = self._backend_tasks.createTaskByUserId(user_id, "task initiated")

      self._debug("createNewCalculationTask", "Result - result: %s" % result)
      return result

    def isCalculationInProgress(self, user_id):
      self._debug("isCalculationInProgress", "Start - user_id: %s" % user_id)
      background_task = self._backend_tasks.getTaskByUserId(user_id)
      result = background_task is not None

      self._debug("isCalculationInProgress", "Finish - result: %s" % result)
      return result