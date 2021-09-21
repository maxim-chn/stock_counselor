from common.backend_tasks.backend_tasks_api import BackendTasksApi
from common.backend_tasks.data_gathering.task import Task, Progress

class BackendTasks(BackendTasksApi):
  """
  Reveals API for backend tasks CRUD.
  It consumes database and message broker APIs.
  """

  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Arguments:
      - service_name -- str.
    """
    super().__init__(service_name, "BackendTasks")
  
  def createTaskBy(self, company_acronym):
    """
    Returns Task.
    Raises RuntimeError.
    Arguments:
      - company_acronym -- str -- unique identifier of a company at a stock exchange.
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
      self._database.createTaskDocument(task.toDocument())
    except RuntimeError as err:
      err_msg = "%s -- createTaskBy -- Failed to persist Task to database.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    
    self._debug("createTaskBy","Finish\nresult:%s" % str(task))
    return task
    
  def deleteTaskBy(self, company_acronym):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - company_acronym -- str -- unique identifier of a company at a stock exchange.
    """
    self._debug("deleteTaskBy", "Start\ncompany_acronym:\t%s" % company_acronym)
    
    try:
      self._database.deleteTaskDocumentBy({ "company_acronym": company_acronym })
    except RuntimeError as err:
      err_msg = "%s -- deleteTaskBy -- Failed to remove Task from database.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    
    self._debug("deleteTaskBy","Finish")
  
  def getTaskBy(self, company_acronym):
    """
    Returns Task or None.
    Raises RuntimeError.
    Arguments:
      - company_acronym -- str -- unique identifier of a company at a stock exchange.
    """
    try:
      self._debug("getTaskBy", "Start\ncompany_acronym:\t%s" % company_acronym)
      result = self._database.readTaskDocumentBy({ "company_acronym": company_acronym })
      if result:
        result = Task.fromDocument(result)
      self._debug("getTaskBy", "Finish\nresult:\t%s" % result)
      return result
    except RuntimeError as err:
      err_msg = "%s -- getTaskBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def updateTaskProgressBy(self, task):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      task -- Task -- backend task.
    """
    try:
      self._debug("updateTaskProgressBy", "Start\ntask:\t%s" % str(task))
      self._database.updateTaskDocument(
        { "progress": task.progress.value },
        { "company_acronym": task.company_acronym }
      )
      self._debug("updateTaskProgressBy", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- updateTaskProgressBy -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
