from data_gathering_main_service.boundary_api import startDataGatheringMainService
from data_gathering_worker_service.worker_api import Worker as DataGatheringWorker
from init_scripts.mongodb import initializeMongoDb
from recommendation_main_service.boundary import startRecommendationMainService
from recommendation_worker_service.worker_api import Worker as RecommendationWorker
from sys import argv

if __name__ == '__main__':
  if argv[1] == "data_gathering_main_service":
    startDataGatheringMainService()
  elif argv[1] == "data_gathering_worker_service":
    DataGatheringWorker().startDataGatheringWorkerService()
  elif argv[1] == "recommendation_main_service":
    startRecommendationMainService()
  elif argv[1] == "recommendation_worker_service":
    RecommendationWorker().startRecommendationWorkerService()
  elif argv[1] == "init_mongodb":
    initializeMongoDb()
