from datetime import datetime
from json import dumps, loads
from traceback import format_exc

class FinancialReport:
  """
  Represents a company's financial report.
  """

  def __init__(self):
    self._class_name = "FinancialReport"
    self._date_format = '%Y-%m-%d'
    self._currency_units = "None"
    self._date = None
    self._measurements = dict()

  @classmethod
  def financialReportWith(cls, currency_units, date, measurements):
    """
    Returns FinancialReport.
    Raises RuntimeError.
    Keyword arguments:
      currency_units -- str.
      date -- datetime.
      measurements -- dict.
    """
    try:
      result = cls()
      result.currency_units = currency_units
      result.date = date
      result.measurements = measurements
      return result
    except Exception as err:
      err_msg = "%s -- financialReportWith -- Failed\n%s" % ("FinancialReport", format_exc(1000, err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromDocument(cls, val):
    """
    Returns FinancialReport.
    Raises RuntimeError.
    Keyword arguments:
      val -- dict -- Document which represents FinancialReport.
    """
    try:
      currency_units = val["currency_units"]
      date = datetime.strptime(val["date"], '%Y-%m-%d')
      measurements = loads(val["measurements"])
      result = cls.financialReportWith(currency_units, date, measurements)
      return result
    except Exception as err:
      err_msg = "%s -- fromDocument -- Failed.\n" % ("FinancialReport", format_exc(1000, err))
      raise RuntimeError(err_msg)
  
  def currencyUnitsUpdated(self):
    """
    Returns bool.
    """
    return not self._currency_units == "None"
  
  def toDocument(self):
    """
    Returns dict.
    Raises RuntimeError.
    """
    try:
      result = {
        "currency_units": self.currency_units,
        "date": self.date.strftime(self._date_format),
        "measurements": dumps(self.measurements)
      }
      return result
    except Exception as err:
      err_msg = "%s -- toDocument -- Failed.\n%s" % (self._class_name, format_exc(1000, err))
      raise RuntimeError(err_msg)

  def __str__(self):
    """
    Returns str.
    Raises RuntimeError.
    """
    return str(self.toDocument())

  # Getters and setters

  @property
  def currency_units(self):
    """
    Returs str.
    """
    return self._currency_units

  @property
  def date(self):
    """
    Returns datetime.
    """
    return self._date

  @property
  def measurements(self):
    """
    Returns dict.
    """
    return self._measurements

  @currency_units.setter
  def currency_units(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      val -- str -- currency units, i.e. USD.
    """
    if val and isinstance(val, str):
      self._currency_units = val
    else:
      raise RuntimeError("%s -- currency_units setter expectes a non-empty str." % self._class_name)

  @date.setter
  def date(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      val -- datetime.
    """
    if val and isinstance(val, datetime):
      self._date = val
    else:
      raise RuntimeError("%s -- date setter expectes a datetime object." % self._class_name)

  @measurements.setter
  def measurements(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      val -- dict -- the key is a date string and the value is financial data.
    """
    if val and isinstance(val, dict):
      self._measurements = val
    else:
      raise RuntimeError("%s -- measurements setter expectes a non-empty dict" % self._class_name)