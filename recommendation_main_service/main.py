"""

"""

from bottle import Bottle, request, response
from recommendation_controller_api import RecommendationControllerApi
import logging
from datetime import datetime
from functools import wraps


def setupLogger():
  logger = logging.getLogger("recommendation_main_service")
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
      logger = logging.getLogger("recommendation_main_service")
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


    @app.route('/investment/recommendations/<user_id>/new')
    def calculate_recommendation(user_id):
      api = RecommendationControllerApi()
      result = api.calculateRecommendation(user_id)
      return result

    app.run(host='localhost', port=8080, quiet=True)
