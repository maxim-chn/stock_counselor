"""Executes the backend tasks that are created by the Data Gathering Main Service"""

from json import dump
import logging
from os import path
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

    company_financial_data = worker.getDataFromSec(acronym)
    if company_financial_data:
      with open(path.join(
          path.dirname(__file__), "remove_in_alpha", "%s.json" % (company_financial_data["acronym"])),
          "w"
        ) as write_file:
          dump(company_financial_data, write_file)

    print("Finished " + acronym)