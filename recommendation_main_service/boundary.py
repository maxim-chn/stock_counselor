"""
This is our Boundary Logic which reveals an external API for a user.
It directly interacts with the bottle module in order to manage a HTTP server.
Some of the user requests are inspected for the expected input that is transferred over to the Controller Logic.
"""

from bottle import Bottle, request, response
from recommendation_main_service.controller_api import RecommendationController
from logging import getLogger, DEBUG, FileHandler, Formatter
from datetime import datetime
from functools import wraps


def setupLogger():
  logger = getLogger("recommendation_main_service")
  logger.setLevel(DEBUG)
  file_handler = FileHandler("recommendation_main_service.log")
  file_handler.setLevel(DEBUG)
  file_handler.setFormatter(Formatter("%(msg)s"))
  logger.addHandler(file_handler)

def log_to_logger(fn):
  """
  Returns the "decoratored" fn.
  Keyword arguments:
    fn -- Function -- the next function that the process is about to execute.
  """
  @wraps(fn)
  def _log_to_logger(*args, **kwargs):
    """
    Decorates the fn parameter. Some data is stored and logged prior and after the fn execution.
    Keyword arguments:
      *args, **kwargs -- basically, arguments intended for the fn.
    """
    request_time = datetime.now()
    actual_response = fn(*args, **kwargs)
    logger = getLogger("recommendation_main_service")
    logger.info("%s -- %s -- %s -- %s -- %s\n" % (
      request.remote_addr,
      request_time,
      request.method,
      request.url,
      response.status
    ))
    return actual_response

  return _log_to_logger

def startRecommendationMainService():
  setupLogger()

  app = Bottle()
  app.install(log_to_logger)

  @app.route("/monitor")
  def monitor():
    return "Hello World!"

  @app.route('/investment/recommendations/<user_id>/new')
  def calculate_recommendation(user_id):
    api = RecommendationController("recommendation_main_service")
    result = api.calculateRecommendation(user_id)
    return result

  app.run(host="localhost", port=8081, quiet=True)
