from common.backend_tasks.backend_tasks_api import BackendTasksApi
from common.backend_tasks.recommendation.task import Task, Progress

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

  def createTaskBy(self, user_id):
    """
    Returns Task.
    Raises RuntimeError.
    Arguments:
      - user_id -- str -- unique user id at the database.
    """
    self._debug("createTaskBy", "Start\nuser_id:\t%s" % user_id)
    task = None

    try:
      task = Task.taskWith(Progress.STARTED, user_id)
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

    self._debug("createTaskBy", "Finish\nresult:\t%s" % str(task))
    return task

  def deleteTaskBy(self, user_id):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      user_id -- str -- unique user id at the database.
    """
    try:
      self._debug("deleteTaskBy", "Start\nuser_id:\t%s" % user_id)
      result = self._database.deleteTaskDocumentBy({ "user_id": user_id })
      self._debug("deleteTaskBy", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- deleteTaskBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def getTaskBy(self, user_id):
    """
    Returns Task or None.
    Raises RuntimeError.
    Arguments:
      user_id -- str -- unique user id at the database.
    """
    try:
      self._debug("getTaskBy", "Start\nuser_id:\t%s" % user_id)
      
      result = self._database.readTaskDocumentBy({ "user_id": user_id })
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
        { "user_id": task.user_id }
      )
      
      self._debug("updateTaskProgressBy", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- updateTaskProgressBy -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
