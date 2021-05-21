from json import dumps, load
from os import path
import pika

from common.loggable_api import Loggable
from common.backend_task_progress import BackendTaskProgress

class BackendTasks(Loggable):
  """
  CRUDs the backend_tasks directly through the file system.
  TODO: implement direct communication with an in-memory database, i.e. Redis, and remove any file system use in v1.0
  """
  def __init__(self, log_id):
    """
    Keyword arguments:
      log_id -- str.
    """
    super().__init__(log_id, "BackendTasks")
    self._config = self._loadRabbitMqConfigurations()


  def createTaskByCompanyAcronym(self, acronym):
    """
    Keyword arguments:
      acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("createTaskByCompanyAcronym", "Start - acronym: %s" % acronym)
    task = {
      "acronym": acronym,
      "progress": BackendTaskProgress.STARTED.value
    }
    message_server_connection = self._getConnectionToRabbitMq(
      self._config["connection"]["host"],
      self._config["connection"]["server_port"],
      self._config["connection"]["vhost"],
      self._config["connection"]["username"],
      self._config["connection"]["password"]
    )
    if message_server_connection:
      channel = message_server_connection.channel()
      channel.queue_declare(queue=self._config["connection"]["channel"]["name"])
      channel.basic_publish(
        exchange=self._config["connection"]["channel"]["exchange"],
        routing_key=self._config["connection"]["channel"]["name"],
        body=dumps(task)
      )
      message_server_connection.close()
      self._debug("createTaskByCompanyAcronym", "Finish - the task has been written")
    else:
      self._debug("createTaskByCompanyAcronym","Finish - the task has not been written")

  def getTaskByCompanyAcronym(self, acronym):
    """
    Returns a dict with the information about a backend task.
    Keyword arguments:
      acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    self._debug("getTaskByCompanyAcronym", "Start - acronym: %s" % acronym)
    result = dict()
    # backend_task_path = self._getBackendTaskPath(acronym)
    # if path.exists(backend_task_path):
    #   with open(backend_task_path, "r") as read_file:
    #     result = load(read_file)
    self._debug("getTaskByCompanyAcronym", "Finish - result: %s" % result)
    return result

  def _getConnectionToRabbitMq(self, host, port, vhost, username, password):
    """
    Returns pika.adapters.blocking_connection.BlockingConnection or None
    """
    self._debug(
      "_getConnectionToRabbitMqQueue",
      "Start - host: %s, port: %s, vhost: %s, username: %s, password: %s" % (
        host, port, vhost, username, password
      )
    )
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(
      host,
      port,
      vhost,
      credentials
    )
    result = pika.BlockingConnection(parameters)
    self._debug("_getConnectionToRabbitMqQueue", "Finish - result: %s" % result)
    return result


  def _loadRabbitMqConfigurations(self):
    self._debug("_loadRabbitMqConfigurations", "Start")
    file_path = path.join(
      path.dirname(__file__),
      "backend_tasks",
      "config.json"
    )
    with open(file_path, "r") as read_file:
      result = load(read_file)
    self._debug("_loadRabbitMqConfigurations", "Finish - result: %s" % result)
    return result