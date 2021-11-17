"""
This is our Boundary Logic which reveals an external API for a user.
It directly interacts with the bottle module in order to manage a HTTP server.
The logic handles the applicative user management requests, i.e. login, signup.
"""

from bottle import Bottle, request, response
from datetime import datetime
from functools import wraps
from logging import getLogger

from applicative_users_service.controller_api import Controller
from applicative_users_service.invalid_credentials_error import InvalidCredentialsError
from common.portfolio_risk_level import PortfolioRiskLevel

def getEmailParamFrom(request):
  """
  Returns str or None.
  Arguments:
    request -- bottle.request
  """
  result = request.query.email
  if not result:
    result = None
  return result

def getFirstNameParamFrom(request):
  """
  Returns str or None.
  Arguments:
    request -- bottle.request
  """
  result = request.query.first_name
  if not result:
    result = None
  return result

def getLastNameParamFrom(request):
  """
  Returns str or None.
  """
  result = request.query.last_name
  if not result:
    result = None
  return result

def getPortfolioRiskLevelFrom(request):
  """
  Returns PortfolioRiskLevel or None.
  """
  risk_level_str = request.query.portfolio_risk_level
  if PortfolioRiskLevel.LOW.value == risk_level_str:
    result = PortfolioRiskLevel.LOW
  elif PortfolioRiskLevel.HIGH.value == risk_level_str:
    result = PortfolioRiskLevel.HIGH
  else:
    result = None
  return result

def startApplicativeUsersService(service_name):
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
      Decorates the fn parameter.
      Some data is stored and logged prior and after the fn execution.
      Keyword arguments:
        *args, **kwargs -- arguments passed for the fn.
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

  @app.route("/existing")
  def login():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET')
    result = "Server error -- Route login failure."
    try:
      controller = Controller(service_name)
      email = getEmailParamFrom(request)
      first_name = getFirstNameParamFrom(request)
      last_name = getLastNameParamFrom(request)
      result = controller.getExistingUserBy(email, first_name, last_name)
    except InvalidCredentialsError as err:
      result += "\n%s" % (str(err))
      getLogger(service_name).error("%s -- %s" % (service_name, result))
    except RuntimeError as err:
      getLogger(service_name).error("%s -- %s\n%s" % (service_name, result, str(err)))
    return result

  @app.route("/new")
  def signup():
    response.set_header('Access-Control-Allow-Origin', '*')
    response.set_header('Access-Control-Allow-Methods', 'GET')
    result = "Server error -- Route signup failure."
    try:
      controller = Controller(service_name)
      email = getEmailParamFrom(request)
      first_name = getFirstNameParamFrom(request)
      last_name = getLastNameParamFrom(request)
      portfolio_risk_level = getPortfolioRiskLevelFrom(request)
      result = controller.newUserBy(email, first_name, last_name, portfolio_risk_level)
    except InvalidCredentialsError as err:
      result += "\n%s" % (str(err))
      getLogger(service_name).error("%s -- %s" % (service_name, result))
    except RuntimeError as err:
      getLogger(service_name).error("%s -- %s\n%s" % (service_name, result, str(err)))
    return result

  app.run(host="localhost", port=3002, quiet=True)
