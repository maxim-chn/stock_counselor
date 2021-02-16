import logging
from time import sleep
from worker_api import WorkerApi

def setupLogger():
  logger = logging.getLogger('data-gathering-worker-service')
  logger.setLevel(logging.DEBUG)
  file_handler = logging.FileHandler('main.log')
  formatter = logging.Formatter('%(msg)s')
  file_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)

if __name__ == '__main__':
  setupLogger()
  worker = WorkerApi()

  while True:
    acronym = worker.getCompanyAcronymForGathering()

    if acronym is None:
      sleep(5)
      continue

    worker.getDataFromSec(acronym)

