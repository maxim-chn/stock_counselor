from data_gathering_main_service.boundary import startDataGatheringMainService
from data_gathering_worker_service.worker_api import Worker
from sys import argv

if __name__ == '__main__':
  if argv[1] == "data_gathering_main_service":
    startDataGatheringMainService()
  elif argv[1] == "data_gathering_worker_service":
    Worker().startDataGatheringWorkerService()