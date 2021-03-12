"""
This is our Boundary logic.
We reveal here the external API for the main service by implementing a HTTP server.
The incoming requests are transfered over to the StockDataMinerController which
holds the Controller logic.
"""

from bottle import Bottle, request, response
from stock_data_miner_controller_api import StockDataMinerControllerApi
import logging
from datetime import datetime
from functools import wraps


def setupLogger():
  logger = logging.getLogger("data_gathering_main_service")
  logger.setLevel(logging.DEBUG)
  file_handler = logging.FileHandler("main.log")
  formatter = logging.Formatter("%(msg)s")
  file_handler.setLevel(logging.DEBUG)
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)

def log_to_logger(fn):
    @wraps(fn)
    def _log_to_logger(*args, **kwargs):
      request_time = datetime.now()
      actual_response = fn(*args, **kwargs)
      logger = logging.getLogger("data_gathering_main_service")
      logger.info('%s %s %s %s %s' % (request.remote_addr,
                                      request_time,
                                      request.method,
                                      request.url,
                                      response.status))
      return actual_response

    return _log_to_logger


if __name__ == '__main__':
    setupLogger()

    app = Bottle()
    app.install(log_to_logger)

    @app.route('/monitor')
    def monitor():
      return "Hello World!"


    @app.route('/collect_stock_data/<acronym_name>')
    def collect_stock_data(acronym_name):
      api = StockDataMinerControllerApi()
      result = api.collectStockData(acronym_name)
      return result

    app.run(host='localhost', port=8080, quiet=True)
