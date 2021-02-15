"""
An assembly of methods that are called by an external actor

"""
from stock_data_miner_controller_file import StockDataMinerController
import logging

class StockDataMinerApi:
    def __init__(self):
      self._controller = StockDataMinerController()
      

    def collectStockData(self, company_acronym):
      msg = '%s - %s() - Start - company_acronym: %s' % (
        "StockDataMinerApi",
        "collectStockData",
        company_acronym
      )
      logging.getLogger('stock_data_miner').debug(msg)

      result = self._controller.collectStockData(company_acronym)

      msg = '%s - %s() - Finish - result: %s' % (
        "StockDataMinerApi",
        "collectStockData",
        result
      )
      logging.getLogger('stock_data_miner').debug(msg)

      return result
