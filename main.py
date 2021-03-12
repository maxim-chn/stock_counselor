from data_gathering_main_service.boundary import startDataGatheringMainService
from sys import argv

if __name__ == '__main__':
  if argv[1] == "data_gathering_main_service":
    startDataGatheringMainService()