from json import load
from os.path import dirname, exists, join
from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from traceback import format_exc

class MessageBrokerApi:
  """
  Reveals API for message broker, i.e. RabbitMQ
  """

  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Keyword argumets:
      service_name -- str
    """
    self._class_name = "MessageBrokerApi"
    self._max_error_chars = 5000
    self._config = self._getRabbitMqConfiguration(service_name)

  def publish(self, message):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      message -- str.
    """
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
        body=message
      )
      connection.close()
    except Exception as err:
      err_msg = "%s -- publish -- Failed\n %s " % (self._class_name, format_exc(self._max_error_chars, err))
      raise RuntimeError(err_msg)
      
  def subscribe(self, callback_function):
    """
    Returns void.
    Raises RuntimeError.
    """
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
      err_msg = "%s -- subscribe -- Failed \n %s " % (self._class_name, format_exc(self._max_error_chars, err))
      raise RuntimeError(err_msg)
  
  def _getRabbitMqConfiguration(self, service_name):
    """
    Returns dict.
    It is a JSON with configurations to connect to RabbitMQ.
    Raises RuntimeError.
    """
    result = dict()
    
    try:
      path_to_config = join(dirname(__file__), "message_broker", "%s.json" % service_name)
      if exists(path_to_config):
        with open(path_to_config, "r") as read_file:
          result = load(read_file)
          read_file.close()
    except Exception as err:
      err_msg = "%s -- _getRabbitMqConfiguration -- Failed to read from the configuration file\nfile_path:\t%s" % (
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)
    
    return result