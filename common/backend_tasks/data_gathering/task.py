from enum import Enum
from json import dumps, JSONDecoder, loads
from traceback import format_exc
from unittest import main, TestCase

max_error_chars = 1000

class Progress(Enum):
  """
  Possible states for the backend task for DataGatheringService
  """
  FINISHED = "Collection completed"
  IN_PROGRESS = "Collection is in progress"
  NOT_EXPECTED = "Collection was not completed as expected"
  NOT_STARTED = "Collection is yet to be started"
  QUERYING_FOR_10K_REPORT_CONTENTS = "Looking for the 10-K Report Contents at the SEC website"
  QUERYING_FOR_10K_IDS = "Looking for Company 10-K Report Ids at the SEC website"
  QUERYING_FOR_AVAILABLE_10K_REPORTS = "Looking for the Available Company 10-K Reports at the SEC website"
  QUERYING_FOR_10K_REPORT = "Looking for the Company 10-K Report at the SEC website"
  QUERYING_FOR_COMPANY_ID = "Looking for the Company Id at the SEC website"
  QUERYING_FOR_FINANCIAL_STMNT_CONTENTS = "Looking for the Financial Statement Contents at the SEC website"
  QUERYING_FOR_FINANCIAL_STMNT_TYPES = "Looking for Company 10-K Financial Statements Types at the SEC website"
  STARTED = "Collection started"

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
      - dct["company_acronym"] -- str.
      - dct["progress"] -- str.
    """
    if "progress" in dct and "company_acronym" in dct:
      company_acronym = dct["company_acronym"]
      progress = Progress(dct["progress"])
      result = Task.taskWith(company_acronym, progress)
      return result

class Task:
  """
  A backend task for the financial data collection.
  """

  def __init__(self):
    self._class_name = "Task"
    self._max_error_chars = max_error_chars
    self._company_acronym = "no company"
    self._progress = Progress.NOT_EXPECTED
  
  @classmethod
  def taskWith(cls, company_acronym, progress):
    """
    Returns Task.
    Raises RuntimeError.
    Arguments:
      company_acronym -- str -- unique identifier of a company at a stock exchange.
      progress -- Progress -- financial data collection progress.
    """
    try:
      result = cls()
      result.company_acronym = company_acronym
      result.progress = progress
      return result
    except RuntimeError as err:
      err_msg = "%s -- taskWith -- Failed.\n%s" % ("Task", str(err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromDocument(cls, val):
    """
    Returns Task.
    Raises RuntimeError.
    Keyword arguments:
      val -- dict -- Document which represents Task.
    """
    try:
      company_acronym = val["company_acronym"]
      progress = Progress(val["progress"])
      return cls.taskWith(company_acronym, progress)
    except RuntimeError as err:
      err_msg = "%s -- fromDocument -- Failed\n%s" % ("Task", str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- fromDocument -- Failed\n%s" % ("Task", format_exc(max_error_chars, err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromJson(cls, val):
    """
    Returns Task.
    Raises RuntimeError.
    Arguments:
      val -- str -- JSON which represents Task.
    """
    try:
      result = loads(val, cls=JsonDecoderForTask)
      return result
    except RuntimeError as err:
      raise RuntimeError("%s -- fromJson -- Failed\n%s" % ("Task", str(err)))
    except Exception as err:
      raise RuntimeError("%s -- fromJson -- Failed\n%s" % ("Task", format_exc(max_error_chars, err)))

  def toDocument(self):
    """
    Returns dict.
    """
    result = {
      "company_acronym": self.company_acronym,
      "progress": self.progress.value
    }
    return result
  
  def toJson(self):
    """
    Returns str.
    Raises RuntimeError.
    """
    try:
      return dumps(self.toDocument())
    except RuntimeError as err:
      err_msg = "%s -- fromJson -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- fromJson -- Failed\n%s" % (self._class_name, format_exc(self._max_error_chars, err))
      raise RuntimeError(err_msg)

  def __str__(self):
    return str(self.toDocument())

  # Getters and setters
  
  @property
  def company_acronym(self):
    """
    Returns str.
    """
    return self._company_acronym
  
  @property
  def progress(self):
    """
    Returns Progress.
    """
    return self._progress

  @company_acronym.setter
  def company_acronym(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      company_acronym -- str -- unique identifier of a company at a stock exchange.
    """
    if val and isinstance(val, str):
      self._company_acronym = val
    else:
      raise RuntimeError("%s -- company_acronym setter expects an argument of type str." % self._class_name)

  @progress.setter
  def progress(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      val -- Progress -- financial data collection progress.
    """
    if val and isinstance(val, Progress):
      self._progress = val
    else:
      raise RuntimeError("%s -- progress setter expects an argument of type Progress." % self._class_name)

# Unit tests

class TestTask(TestCase):
  def test_toJson(self):
    task = Task.taskWith("msft", Progress.NOT_STARTED)
    expected_json = "{\"company_acronym\": \"%s\", \"progress\": \"%s\"}" % (
      task.company_acronym, task.progress.value
    )
    self.assertEqual(str(expected_json), str(task.toJson()))

  def test_fromJson(self):
    task_expected = Task.taskWith("msft", Progress.NOT_STARTED)
    task = Task.fromJson(task_expected.toJson())
    self.assertEqual(task_expected.company_acronym, task.company_acronym)
    self.assertEqual(task_expected.progress, task.progress)

if __name__ == '__main__':
  main()