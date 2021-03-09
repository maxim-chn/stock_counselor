"""
Executes the backend tasks that are created by the Recommendation Main Service
"""

import logging
from time import sleep
from worker_api import WorkerApi

def setupLogger():
  logger = logging.getLogger('recommendation-worker-service')
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
    user_id = worker.getUserIdForGathering()

    if user_id is None:
      sleep(5)
      continue

    worker.calculateRecommendationByUserId(user_id)
    print("Finished " + user_id)
    exit(0)