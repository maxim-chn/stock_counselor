from logging import getLogger

class Loggable:

  def __init__(self, class_name):
    self._class_name = class_name
    self._log_id = "recommendation-worker-service"

  def _error(self, function_name, message):
    to_log = "%s - %s() - Error - %s" % (self._class_name, function_name, message)
    getLogger(self._log_id).error(to_log)

  def _debug(self, function_name, message):
    to_log = "%s - %s() - Debug - %s" % (self._class_name, function_name, message)
    getLogger(self._log_id).debug(to_log)

  def _info(self, function_name, message):
    to_log = "%s - %s() - Info - %s" % (self._class_name, function_name, message)
    getLogger(self._log_id).info(to_log)