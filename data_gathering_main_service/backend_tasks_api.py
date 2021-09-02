from json import dump, load
from os import path
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from traceback import format_exc

from common.loggable_api import Loggable
from common.backend_task_progress import BackendTaskProgress

class BackendTasks(Loggable):
  """
  CRUDs the backend_tasks directly through the file system.
  TODO: implement direct communication with an in-memory database, i.e. Redis, and remove any file system use in v1.0
  """
  def __init__(self, log_id):
    """
    Returns BackendTasks object.
    Throws RuntimeError exception.
    Keyword arguments:
      log_id -- str.
    """
    super().__init__(log_id, "BackendTasks")
    self._config = self._getRabbitMqConfiguration()

  def consumeTestMessage(self, callback_function):
    """
    Returns void.
    Throws RuntimeError exception.
    """
    self._debug("consumeTestMessage", "Start")
    try:
      credentials = PlainCredentials(self._config["username"], self._config["password"])
      parameters = ConnectionParameters(
        self._config["host"],
        self._config["server_port"],
        self._config["vhost"],
        credentials
      )
      connection = BlockingConnection(parameters)
      channel = connection.channel()
      channel.queue_declare(queue=self._config["channel"]["name"])
      channel.basic_consume(
        queue=self._config["channel"]["name"],
        auto_ack=True,
        on_message_callback=callback_function
      )
      channel.start_consuming()
      connection.close()
    except Exception as err:
      err_msg = "BackendTasks -- consumeTestMessage -- Failed \n %s " % format_exc(err)
      raise RuntimeError(err_msg)
    finally:
      self._debug("consumeTestMessage", "Finish")
  
  def createTaskByCompanyAcronym(self, acronym):
    """
    Returns void.
    Keyword arguments:
      acronym -- str -- unique identifier of a company at a stock exchange.
    """
    self._debug("createTaskByCompanyAcronym", "Start\nacronym:\t%s" % acronym)
    task = {
      "acronym": acronym,
      "progress": BackendTaskProgress.STARTED.value
    }
    backend_task_path = self._getBackendTaskPath(acronym)
    with open(backend_task_path, "w+") as write_file:
        dump(task, write_file)
    self._debug("createTaskByCompanyAcronym","Finish")

  def getTaskByCompanyAcronym(self, acronym):
    """
    Returns dict.
    It is a JSON with data about backend task.
    Keyword arguments:
      acronym -- str -- unique identifier of a company at a stock exchange.
    """
    self._debug("getTaskByCompanyAcronym", "Start\nacronym:\t%s" % acronym)
    result = dict()
    backend_task_path = self._getBackendTaskPath(acronym)
    if path.exists(backend_task_path):
      with open(backend_task_path, "r") as read_file:
        result = load(read_file)
    self._debug("getTaskByCompanyAcronym", "Finish\nresult:\t%s" % result)
    return result

  def publishTestMessage(self):
    """
    Returns void.
    Throws RuntimeError exception.
    """
    self._debug("publishTestMessage", "Start")
    try:
      credentials = PlainCredentials(self._config["username"], self._config["password"])
      parameters = ConnectionParameters(
        self._config["host"],
        self._config["server_port"],
        self._config["vhost"],
        credentials
      )
      connection = BlockingConnection(parameters)
      channel = connection.channel()
      response = channel.queue_declare(self._config["channel"]["name"])
      channel.queue_bind(exchange=self._config["channel"]["exchange"], queue=response.method.queue)
      channel.basic_publish(
        exchange=self._config["channel"]["exchange"],
        routing_key=self._config["channel"]["name"],
        body="Test message"
      )
      connection.close()
    except Exception as err:
      err_msg = "BackendTasks -- publishTestMessage -- Failed \n %s " % format_exc(1000, err)
      raise RuntimeError(err_msg)
    finally:
      self._debug("publishTestMessage", "Finish")
  
  def _getBackendTaskPath(self, company_acronym):
    """
    TODO: remove in v1.0.
    Returns the path to the file with the backend_task in the file-system.
    Keyword arguments:
      company_acronym -- str -- an unique identifier of a company at a stock exchange (i.e. NASDAQ).
    """
    return path.join(
      path.dirname(__file__),
      "..",
      "common",
      "backend_tasks_db",
      "data_gathering",
      "%s.json" % company_acronym
    )

  def _getRabbitMqConfiguration(self):
    """
    Returns dict.
    It is a JSON with configurations to connect to RabbitMQ.
    Throws RuntimeError exception.
    """
    self._debug("_getRabbitMqConfiguration", "Start")
    result = dict()
    try:
      config_path = path.join(path.dirname(__file__), "backend_tasks", "rabbitmq_config.json")
      if path.exists(config_path):
        with open(config_path, "r") as read_file:
          result = load(read_file)
          read_file.close()
    except Exception as err:
      err_msg = "BackendTasks -- _getRabbitMqConfiguration -- Failed to read from"
      err_msg = "%s\nfile_path:\t %s " % (err_msg, format_exc(1000, err))
      raise RuntimeError(err_msg)
    finally:
      self._debug("_getRabbitMqConfiguration", "Finish\nresult:\t%s" % result)
    return result
