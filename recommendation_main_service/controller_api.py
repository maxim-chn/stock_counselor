from common.investment_recommendation import InvestmentRecommendation
from common.recommendation_backend_tasks_api import BackendTasks
from common.backend_tasks.recommendation.task import Progress
from common.database_api import DatabaseApi
from common.loggable_api import Loggable

class Controller(Loggable):
  """
  This is our Controller logic.
  It reveals an internal API with the methods that map an input from the Boundary to the backend task.
  The backend tasks are related to the Investment Recommendation Calculation.
  The backend task will later be picked up by an external worker service.
  """
  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Arguments:
      log_id -- str.
    """
    super().__init__(service_name, "Controller")
    self._backend_tasks = BackendTasks(service_name)
    self._database = DatabaseApi(service_name)

  def calculateRecommendationFor(self, user_id):
    """
    Returns a str.
    Raises RuntimeError.
    It represents the backend task progress for the investment recommendation calculation for a certain user.
    Arguments:
      - user_id -- str -- unique user id at the database.
    """
    self._debug("calculateRecommendationFor", "Start\nuser_id:\t%s" % user_id)
    
    try:
      progress = self._calculationProgressFor(user_id)
    except RuntimeError as err:
      err_msg = "%s -- calculateRecommendationFor" % self._class_name
      err_msg += " -- Failed at retrieving investment recommendation calculation progress.\n%s" % str(err)
      raise RuntimeError(err_msg)

    if progress == Progress.NOT_STARTED:
      try:
        task = self._backend_tasks.createTaskBy(user_id)
        result = task.progress.value
      except RuntimeError as err:
        err_msg = "%s -- calculateRecommendationFor" % self._class_name
        err_msg += " -- Failed at creating a new backend task" % str(err)
        raise RuntimeError(err_msg)
    else:
      result = progress.value
    
    self._debug("calculateRecommendationFor", "Finish\nresult:\t%s" % result)
    return result

  def stopCalculatingRecommendationFor(self, user_id):
    """
    Returns str.
    Raises RuntimeError.
    Removes the backend task for recommendation calculation from the database.
    Arguments:
      - user_id -- str -- unique user id at the database.
    """
    self._debug("stopCalculatingRecommendationFor", "Start\nuser_id:\t%s" % user_id)
    result = "No task was found"
    
    try:
      progress = self._calculationProgressFor(user_id)
    except RuntimeError as err:
      err_msg = "%s -- stopCalculatingRecommendationFor" % self._class_name
      err_msg += " -- Failed at retrieving investment recommendation calculation progress.\n%s" % str(err)
      raise RuntimeError(err_msg)

    if not progress == Progress.NOT_STARTED:
      try:
        self._backend_tasks.deleteTaskBy(user_id)
        result = "The task was removed"
      except RuntimeError as err:
        err_msg = "%s -- stopCalculatingRecommendationFor" % self._class_name
        err_msg += " -- Failed at deleting a backend task" % str(err)
        raise RuntimeError(err_msg)
    
    self._debug("stopCalculatingRecommendationFor", "Finish\nresult:\t%s" % result)
    return result

  def summaryOfInvestmentRecommendations(self, user_id):
    """
    Returns str.
    Raises RuntimeError.
    Returns the collection of InvestmentRecommendations as JSON for the user.
    Arguments:
      - user_id -- str -- unique user id at the database.
    """
    function_name = "summaryOfInvestmentRecommendations"
    self._debug(function_name, "Start\nuser_id:\t%s" % user_id)
    result = "["

    try:
      filterBy = { "user_id": user_id }
      investment_recommendation_documents = self._database.readInvestmentRecommendationDocumentsBy(filterBy)
    except RuntimeError as err:
      err_msg = "%s -- %s -- Failed at retrieving investment recommendation documents for the user.\n%s" % (
        self._class_name,
        function_name,
        str(err)
      )
      raise RuntimeError(err_msg)

    try:
      for document in investment_recommendation_documents:
        investment_recommendation = InvestmentRecommendation.fromDocument(document)
        if len(result) < 2:
          result += investment_recommendation.toJson()
        else:
          result += ",%s" % investment_recommendation.toJson()
      result += "]"
    except RuntimeError as err:
      err_msg = "%s -- %s -- Failed at mapping investment_recommendation_document to JSON.\n%s" % (
        self._class_name,
        function_name,
        str(err)
      )
      raise RuntimeError(err_msg)

    self._debug(function_name, "Finish\nResult:\t%s" % result)
    return result

  def _calculationProgressFor(self, user_id):
    """
    Returns Progress.
    Raises RuntimeError.
    Arguments:
      - user_id -- str -- an unique identifier of a user inside our program.
    """
    try:
      self._debug("_calculationProgress", "Start\nuser_id:\t%s" % user_id)
      
      task = self._backend_tasks.getTaskBy(user_id)
      if not task:
        result = Progress.NOT_STARTED
      else:
        result = task.progress
      
      self._debug("_calculationProgress", "Finish\nresult:\t%s" % result)
      return result
    except RuntimeError as err:
      raise RuntimeError("%s -- _calculationProgressFor -- Failed\n%s" % (self._class_name, str(err)))
