from logging import getLogger, DEBUG, FileHandler, Formatter
from os.path import join, dirname, exists
from sys import argv
from traceback import format_exc

from applicative_users_service.boundary_api import startApplicativeUsersService
from common.data_gathering_backend_tasks_api import BackendTasks as DataGatheringBackendTasks
from common.recommendation_backend_tasks_api import BackendTasks as RecommendationBackendTasks
from data_gathering_main_service.boundary_api import startDataGatheringMainService
from data_gathering_worker_service.worker_api import startDataGatheringWorkerService
from recommendation_main_service.boundary_api import startRecommendationMainService
from recommendation_worker_service.worker_api import startRecommendationWorkerService

available_services = [
  "applicative_users_service",
  "data_gathering_main_service",
  "data_gathering_worker_service",
  "recommendation_main_service",
  "recommendation_worker_service"
  ]

def getBackendTasks(service_name):
  """
  Returns data_gathering_main_service.backend_tasks_api.BackendTasks or
          data_gathering_worker_service.backend_tasks_api.BackendTasks or
          recommendation_main_service.backend_tasks_api.BackendTasks or
          recommendation_worker_service.backend_tasks_api.BackendTasks or
          None
  Raises RuntimeError.
  Arguments:
    service_name -- str.
  """
  if service_name == available_services[0]:
    return None
  if service_name == available_services[1] or service_name == available_services[2]:
    return DataGatheringBackendTasks(service_name)
  if service_name == available_services[3] or service_name == available_services[4]:
    return RecommendationBackendTasks(service_name)
  err_msg = "%s -- getBackendTasks -- Failed to map service_name to the relevant backend tasks object." % service_name
  raise RuntimeError(err_msg)

def logDebug(service_name, message):
  """
  Returns void
  """
  logger = getLogger(service_name)
  logger.error("%s -- DEBUG -- %s" % (service_name, message))

def logError(service_name, message):
  """
  Returns void
  """
  logger = getLogger(service_name)
  logger.error("%s -- ERROR -- %s" % (service_name, message))

def setupLogger(service_name):
  """
  Returns void.
  Creates a logger object for the application.
  """
  log_path = join(dirname(__file__), "%s.log" % service_name)
  if exists(log_path):
    with open(log_path, "w") as write_file:
      write_file.close()
  logger = getLogger(service_name)
  logger.setLevel(DEBUG)
  file_handler = FileHandler("%s.log" % service_name)
  file_handler.setLevel(DEBUG)
  file_handler.setFormatter(Formatter("%(msg)s"))
  logger.addHandler(file_handler)

def startService(service_name):
  """
  Returns void.
  Raises RuntimeError.
  Arguments:
    service_name -- str.
  """
  function_name = "start_service"
  try:
    if service_name == available_services[0]:
      startApplicativeUsersService(service_name)
    elif service_name == available_services[1]:
      startDataGatheringMainService(service_name)
    elif service_name == available_services[2]:
      startDataGatheringWorkerService(service_name)
    elif service_name == available_services[3]:
      startRecommendationMainService(service_name)
    elif service_name == available_services[4]:
      startRecommendationWorkerService(service_name)
    else:
      raise RuntimeError("Failed to map the service name to the relevant service object.")
  except RuntimeError as err:
    err_msg = "%s -- %s -- Failed.\n%s" % (service_name, function_name, str(err))
    getLogger(service_name).error(err_msg)


if __name__ == '__main__':
  service_name = argv[1]
  
  if service_name not in available_services:
    print("Please specify one of the following services\n%s" % available_services)
    exit(1)

  expected_message = "Test message"
  max_error_chars = 5000

  def uponValidatedMessageBroker(ch, method, properties, body):
    """
    Returns void.
    Arguments:
      ch -- Channel -- RabbitMq channel.
      method -- ??? -- ???
      properties -- ??? -- ???
      body -- ??? -- contains the message.
    """
    try:
      if expected_message in str(body):
        ch.stop_consuming()
      else:
        raise RuntimeError("Expected test message was not consumed from message broker")
    except Exception as err:
      err_msg = "Failed during message broker message consumption\n%s" % format_exc(max_error_chars, err)
      logError(service_name, err_msg)
      exit(1)
    finally:
      ch.stop_consuming()
  
  try:
    setupLogger(service_name)
    
    backend_tasks = getBackendTasks(service_name)
    
    if backend_tasks:
      logDebug(service_name, "Started message broker test")
      backend_tasks.publishTestMessage()
      backend_tasks.consumeMessage(uponValidatedMessageBroker)
      logDebug(service_name, "Ended message broker test\n")

      logDebug(service_name, "Started database test")
      backend_tasks.createTestDocument()
      backend_tasks.deleteTestDocument()
      logDebug(service_name, "Ended database test\n")
    
      backend_tasks = None
    
    startService(service_name)
  except RuntimeError as err:
    err_msg = "Failed to start the service\n%s" % str(err)
    logError(service_name, err_msg)
    exit(1)
