from common.database_api import DatabaseApi
from common.loggable_api import Loggable
from common.message_broker_api import MessageBrokerApi

class BackendTasksApi(Loggable):
  """
  This is an abstract class.
  It contains logic common to any backend tasks class.
  """

  def __init__(self, service_name, descendant_class_name):
    """
    Raises RuntimeError.
    Arguments:
      - service_name -- str.
      - descendant_class_name -- str.
    """
    super().__init__(service_name, descendant_class_name)
    self._database = DatabaseApi(service_name)
    self._message_broker = MessageBrokerApi(service_name)

  def consumeMessage(self, callback_function):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - callback_function -- Function -- Execution steps upon receiving a message from message broker.
    """
    try:
      self._debug("consumeMessage", "Start")
      
      self._message_broker.subscribe(callback_function)
      
      self._debug("consumeMessage", "Finish")
    except Exception as err:
      err_msg = "%s -- consumeMessage -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def createTestDocument(self):
    """
    Returns void.
    Raises RuntimeError.
    """
    try:
      self._debug("createTestDocument", "Start")
      
      self._database.createTestDocument({"field_a": "value_a"})
      
      self._debug("createTestDocument", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- createTestDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def deleteTestDocument(self):
    """
    Returns void.
    Raises RuntimeError.
    """
    try:
      self._debug("deleteTestDocument", "Start")
      
      self._database.deleteTestDocumentBy({"field_a": "value_a"})
      
      self._debug("deleteTestDocument", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- deleteTestDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def publishTestMessage(self):
    """
    Returns void.
    Raises RuntimeError.
    """
    try:
      self._debug("publishTestMessage", "Start")
      
      self._message_broker.publish("Test message")
      
      self._debug("publishTestMessage", "Finish")
    except Exception as err:
      err_msg = "%s -- publishTestMessage -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    