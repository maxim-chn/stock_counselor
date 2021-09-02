from logging import getLogger, DEBUG, FileHandler, Formatter
from os.path import join, dirname, exists
from sys import argv

from data_gathering_main_service.boundary_api import startDataGatheringMainService
from data_gathering_main_service.backend_tasks_api import BackendTasks as DataGatheringMainServiceBackendTasks
from data_gathering_worker_service.worker_api import Worker as DataGatheringWorker
from recommendation_main_service.boundary import startRecommendationMainService
from recommendation_worker_service.worker_api import Worker as RecommendationWorker

def logError(service_name, err):
  """
  Returns void
  """
  logger = getLogger(service_name)
  logger.error("%s -- ERROR\n%s" % (service_name, str(err)))

def uponValidatedMessageBrokerForDataGatheringMainService(ch, method, properties, body):
  """
  Returns void
  """
  expected_message = "Test message"
  service_name = "data_gathering_main_service"
  try:
    if expected_message in str(body):
      ch.stop_consuming()
    else:
      raise RuntimeError("Expected test message was not consumed from message broker")
  except RuntimeError as err:
    logError(service_name, err)
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
      backend_tasks = DataGatheringMainServiceBackendTasks(argv[1])
      backend_tasks.publishTestMessage()
      backend_tasks.consumeTestMessage(uponValidatedMessageBrokerForDataGatheringMainService)
      startDataGatheringMainService()
    except RuntimeError as err:
      logError(argv[1], err)
      exit(1)
  elif argv[1] == "data_gathering_worker_service":
    DataGatheringWorker().startDataGatheringWorkerService()
  elif argv[1] == "recommendation_main_service":
    startRecommendationMainService()
  elif argv[1] == "recommendation_worker_service":
    RecommendationWorker().startRecommendationWorkerService()
