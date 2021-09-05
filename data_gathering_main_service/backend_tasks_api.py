from common.loggable_api import Loggable
from common.message_broker_api import MessageBrokerApi
from data_gathering_main_service.backend_tasks.task import Progress, Task

class BackendTasks(Loggable):
  """
  Reveals API for backend tasks CRUD.
  It consumes database and message broker APIs.
  """
  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Keyword arguments:
      service_name -- str.
    """
    super().__init__(service_name, "BackendTasks")
    self._message_broker = MessageBrokerApi(service_name)
    self._database = None # TODO: initialize database communicator

  def consumeTestMessage(self, callback_function):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      callback_function -- Function -- Execution steps upon receiving a message from message broker.
    """
    self._debug("consumeTestMessage", "Start")
    
    try:
      self._message_broker.subscribe(callback_function)
    except Exception as err:
      err_msg = "%s -- consumeTestMessage -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    
    self._debug("consumeTestMessage", "Finish")
  
  def createTaskBy(self, company_acronym):
    """
    Returns Task.
    Raises RuntimeError.
    Keyword arguments:
      company_acronym -- str -- unique identifier of a company at a stock exchange.
    """
    self._debug("createTaskBy", "Start\ncompany_acronym:\t%s" % company_acronym)
    task = None
    
    try:
      task = Task.taskWith(company_acronym, Progress.STARTED)
    except RuntimeError as err:
      err_msg = "%s -- createTaskBy -- Failed to initialize Task object.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    
    try:
      self._message_broker.publish(task.toJson())
    except RuntimeError as err:
      err_msg = "%s -- createTaskBy -- Failed to publish Task to message broker.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

    try:
      pass
      # TODO: store in database
    except RuntimeError as err:
      err_msg = "%s -- createTaskBy -- Failed to persist Task to database.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    
    self._debug("createTaskBy","Finish\ntask:%s" % str(task))
    return task

  def getTaskBy(self, company_acronym):
    """
    Returns Task or None.
    Raises RuntimeError.
    Keyword arguments:
      company_acronym -- str -- unique identifier of a company at a stock exchange.
    """
    self._debug("getTaskBy", "Start\nacronym:\t%s" % company_acronym)
    result = None
    
    try:
      pass
      # TODO: retrieve from database
    except RuntimeError:
      err_msg = "%s -- getTaskBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    
    self._debug("getTaskBy", "Finish\nresult:\t%s" % result)
    return result

  def publishTestMessage(self):
    """
    Returns void.
    Raises RuntimeError.
    """
    self._debug("publishTestMessage", "Start")
    
    try:
      self._message_broker.publish("Test message")
    except Exception as err:
      err_msg = "%s -- publishTestMessage -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    
    self._debug("publishTestMessage", "Finish")