from logging import getLogger, DEBUG, FileHandler, Formatter
from os.path import join, dirname, exists
from sys import argv

from data_gathering_main_service.backend_tasks_api import BackendTasks as DataGatheringServiceBackendTasks
from data_gathering_main_service.boundary_api import startDataGatheringMainService
from data_gathering_worker_service.worker_api import Worker as DataGatheringWorker
from recommendation_main_service.boundary import startRecommendationMainService
from recommendation_worker_service.worker_api import Worker as RecommendationWorker

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

def uponValidatedMessageBrokerForDataGatheringMainService(ch, method, properties, body):
  """
  Returns void.
  Keyword arguments:
    ch -- Channel -- RabbitMq channel.
    method -- ??? -- ???
    properties -- ??? -- ???
    body -- ??? -- contains the message.
  """
  expected_message = "Test message"
  service_name = "data_gathering_main_service"
  try:
    if expected_message in str(body):
      ch.stop_consuming()
    else:
      raise RuntimeError("Expected test message was not consumed from message broker")
  except Exception as err:
    err_msg = "Failed during message broker message consumption\n%s" % str(err)
    logError(service_name, err_msg)
    exit(1)
  finally:
    ch.stop_consuming()

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

if __name__ == '__main__':
  if argv[1] == "data_gathering_main_service":
    setupLogger(argv[1])
    try:
      backend_tasks = DataGatheringServiceBackendTasks(argv[1])
      
      logDebug(argv[1], "Started message broker test")
      backend_tasks.publishTestMessage()
      backend_tasks.consumeTestMessage(uponValidatedMessageBrokerForDataGatheringMainService)
      logDebug(argv[1], "Ended message broker test\n")

      logDebug(argv[1], "Started database test")
      backend_tasks.createTestDocument()
      backend_tasks.deleteTestDocument()
      logDebug(argv[1], "Ended database test\n")
      
      backend_tasks = None
      startDataGatheringMainService(argv[1])
    except RuntimeError as err:
      err_msg = "Failed to start the service\n%s" % str(err)
      logError(argv[1], err_msg)
      exit(1)
  elif argv[1] == "data_gathering_worker_service":
    DataGatheringWorker().startDataGatheringWorkerService()
  elif argv[1] == "recommendation_main_service":
    startRecommendationMainService()
  elif argv[1] == "recommendation_worker_service":
    RecommendationWorker().startRecommendationWorkerService()
