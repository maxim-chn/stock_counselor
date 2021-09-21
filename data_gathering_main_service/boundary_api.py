"""
This is our Boundary Logic which reveals an external API for a user.
It directly interacts with the bottle module in order to manage a HTTP server.
Some of the user requests are inspected for the expected input that is transferred over to the Controller Logic.
"""

from bottle import Bottle, request, response
from data_gathering_main_service.controller_api import Controller
from datetime import datetime
from functools import wraps
from logging import getLogger

def startDataGatheringMainService(service_name):
  """
  Returns void.
  Starts the Bottle server.
  Raises RuntimeError.
  Arguments:
    service_name -- str.
  """
  def log_to_logger(fn):
    """
    Returns Function.
    It is decorated to log HTTP responses.
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
      logger = getLogger(service_name)
      logger.info("%s -- %s -- %s -- %s -- %s\n" % (
        request.remote_addr,
        request_time,
        request.method,
        request.url,
        response.status
      ))
      return actual_response

    return _log_to_logger
  
  app = Bottle()
  app.install(log_to_logger)

  @app.route("/monitor")
  def monitor():
    return "Hello World!"

  @app.route("/cancel_stock_data_collection/<acronym_name>")
  def cancel_stock_data_collection(acronym_name):
    result = "Server error"
    try:
      controller = Controller(service_name)
      result = controller.stopCollectingFinancialDataFor(acronym_name)
    except RuntimeError as err:
      getLogger(service_name).error("%s -- Server error.\n%s" % (service_name, str(err)))
    return result

  @app.route("/collect_stock_data/<acronym_name>")
  def collect_stock_data(acronym_name):
    result = "Server error"
    try:
      controller = Controller(service_name)
      result = controller.collectFinancialDataFor(acronym_name)
    except RuntimeError as err:
      getLogger(service_name).error("%s -- Server error\n%s" % (service_name, str(err)))
    return result

  app.run(host="localhost", port=3000, quiet=True)
