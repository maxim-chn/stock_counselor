from enum import Enum
from json import dumps, JSONDecoder, loads
from traceback import format_exc
from unittest import main, TestCase

max_error_chars = 1000

class Progress(Enum):
  """
  Possible states for the backend task for RecommendationService
  """
  FINISHED = "Recommendation completed"
  IN_PROGRESS = "Recommendation is in progress"
  NOT_EXPECTED = "Recommendation was not completed as expected"
  NOT_STARTED = "Recommendation is yet to be started"
  STARTED = "Recommendation started"

class JsonDecoderForTask(JSONDecoder):
  """
  Custom JSON decoder from str to Task.
  """
  def __init__(self, *args, **kwargs):
    JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
  
  def object_hook(self, dct):
    """
    Returns Task.
    Raises RuntimeError.
    Keyword arguments:
      - dct["progress"] -- str.
      - dct["user_id"] -- str.
    """
    if "progress" in dct and "user_id" in dct:
      progress = Progress(dct["progress"])
      user_id = dct["user_id"]
      result = Task.taskWith(progress, user_id)
      return result

class Task:
  """
  A backend task for investment recommendation.
  """

  def __init__(self):
    self._class_name = "Task"
    self._max_error_chars = max_error_chars
    self._progress = Progress.NOT_EXPECTED
    self._user_id = "None"

  @classmethod
  def taskWith(cls, progress, user_id):
    """
    Returns Task.
    Raises RuntimeError.
    Arguments:
      - progress -- Progress.
      - user_id -- str.
    """
    try:
      result = cls()
      result.progress = progress
      result.user_id = user_id
      return result
    except Exception as err:
      err_msg = "%s -- taskWith -- Failed\n%s" % ("Task", format_exc(max_error_chars, err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromDocument(cls, val):
    """
    Returns Task.
    Raises RuntimeError.
    Keyword arguments:
      - val["progress"] -- str.
      - val["user_id"] -- str.
    """
    try:
      progress = Progress(val["progress"])
      user_id = val["user_id"]
      result = Task.taskWith(progress, user_id)
      return result
    except Exception as err:
      err_msg = "%s -- fromDocument -- Failed\n%s" % ("Task", format_exc(max_error_chars, err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromJson(cls, val):
    """
    Returns Task.
    Raises RuntimeError.
    Arguments:
      - val -- str -- JSON representation of Task.
    """
    try:
      result = loads(val, cls=JsonDecoderForTask)
      return result
    except RuntimeError as err:
      err_msg = "%s -- fromJson -- Failed\n%s" % ("Task", str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- fromJson -- Failed\n%s" % ("Task", format_exc(max_error_chars, err))
      raise RuntimeError(err_msg)

  def toDocument(self):
    """
    Returns dict.
    """
    result = {
      "progress": self.progress.value,
      "user_id": self.user_id
    }
    return result

  def toJson(self):
    """
    Returns str.
    Raises RuntimeError.
    """
    try:
      result = dumps(self.toDocument())
      return result
    except RuntimeError as err:
      err_msg = "%s -- fromJson -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- fromJson -- Failed\n%s" % (self._class_name, format_exc(self._max_error_chars, err))
      raise RuntimeError(err_msg)

  def __str__(self):
    """
    Returns str.
    """
    return str(self.toDocument())

  # Getters and setters

  @property
  def progress(self):
    """
    Returns Progress.
    """
    return self._progress
  
  @property
  def user_id(self):
    """
    Returns str.
    """
    return self._user_id

  @progress.setter
  def progress(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - val -- Progress.
    """
    if val and isinstance(val, Progress):
      self._progress = val
    else:
      raise RuntimeError("%s -- progress setter expects an argument of type Progress" % self._class_name)
  
  @user_id.setter
  def user_id(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - val -- str.
    """
    if val and isinstance(val, str):
      self._user_id = val
    else:
      raise RuntimeError("%s -- user_id setter expects an argument of type str" % self._class_name)

# Unit tests

class TestTask(TestCase):
  def test_toJson(self):
    task = Task.taskWith(Progress.NOT_STARTED, "uuid")
    expected_json = "{\"progress\": \"%s\", \"user_id\": \"%s\"}" % (task.progress.value, task.user_id)
    self.assertEqual(str(expected_json), str(task.toJson()))

  def test_fromJson(self):
    task_expected = Task.taskWith(Progress.NOT_STARTED, "uuid")
    task = Task.fromJson(task_expected.toJson())
    self.assertEqual(task_expected.progress, task.progress)
    self.assertEqual(task_expected.user_id, task.user_id)

if __name__ == '__main__':
  main()