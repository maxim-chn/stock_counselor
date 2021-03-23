from common.backend_task_progress import BackendTaskProgress
from common.loggable_api import Loggable
from enum import Enum
from recommendation_main_service.backend_tasks_api import BackendTasks

class CalculationProgress(Enum):
  STARTED = "Investment Recommendation Calculation has been Started"
  IN_PROGRESS = "Investment Recommendation Calculation is in Progress"
  FINISHED = "Investment Recommendation has been Calculated"

class RecommendationController(Loggable):
  """
  This is our Controller logic.
  It reveals an internal API with the methods that map an input from the Boundary to the backend task.
  The backend tasks are related to the Investment Recommendation Calculation.
  The backend task will later be picked up by an external worker service.
  """
  def __init__(self, log_id):
    """
    Keyword arguments:
      log_id -- str.
    """
    super().__init__(log_id, "RecommendationController")
    self._backend_tasks = BackendTasks(log_id)

  def calculateRecommendation(self, user_id):
    """
    Returns a str.
    It represents the backend task progress for the investment recommendation calculation for a certain user.
    Keyword arguments:
      user_id -- str -- unique identifier of a user inside our program.
    """
    self._debug("calculateRecommendation", "Start - user_id: %s" % user_id)
    progress = self._calculationProgress(user_id)
    if not progress:
      self._backend_tasks.createTaskByUserId(user_id)
      result = CalculationProgress.STARTED.value
    elif progress == BackendTaskProgress.FINISHED.value:
      result = CalculationProgress.FINISHED.value
    else:
      result = CalculationProgress.IN_PROGRESS.value
    self._debug("calculateRecommendation", "Finish - result: %s\n" % result)
    return result

  def _calculationProgress(self, user_id):
    """
    Returns a str or None.
    The str is a value of the BackendTaskProgress Enum.
    Keyword arguments:
      user_id -- str -- an unique identifier of a user inside our program.
    """
    self._debug("_calculationProgress", "Start - user_id: %s" % user_id)
    background_task = self._backend_tasks.getTaskByUserId(user_id)
    if not "progress" in background_task.keys():
      result = None
    else:
      result = background_task["progress"]
    self._debug("_calculationProgress", "Finish - result: %s" % result)
    return result