from datetime import datetime
from json import load
from os.path import dirname, exists, join
from re import match
from traceback import format_exc

class FinancialReport:
  """
  Represents a company's financial report.
  """
  class_name = "FinancialReport"
  date_format = '%Y-%m-%d'
  max_error_chars = 1000

  def __init__(self):
    self._company_acronym = None
    self._currency_units = None
    self._date = None
    self._measurements = dict()
    self._regex = self._getFinancialIndicatorsRegEx()

  @classmethod
  def financialReportWith(cls, company_acronym, currency_units, date, measurements):
    """
    Returns FinancialReport.
    Raises RuntimeError.
    Arguments:
      - company_acronym -- str.
      - currency_units -- str.
      - date -- datetime.
      - measurements -- dict.
    """
    try:
      result = cls()
      result.company_acronym = company_acronym
      result.currency_units = currency_units
      result.date = date
      result.measurements = measurements
      return result
    except RuntimeError as err:
      err_msg = "%s -- financialReportWith -- Failed\n%s" % (FinancialReport.class_name, str(err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromDocument(cls, val):
    """
    Returns FinancialReport.
    Raises RuntimeError.
    Arguments:
      val -- dict -- Document which represents FinancialReport.
    """
    try:
      company_acronym = val["company_acronym"]
      currency_units = val["currency_units"]
      date = datetime.strptime(val["date"], FinancialReport.date_format)
      measurements = val["measurements"]
      result = cls.financialReportWith(company_acronym, currency_units, date, measurements)
      return result
    except RuntimeError as err:
      err_msg = "%s -- fromDocument -- Failed\n%s" % (FinancialReport.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- fromDocument -- Failed.\n" % (
        FinancialReport.class_name, format_exc(FinancialReport.max_error_chars, err)
      )
      raise RuntimeError(err_msg)
  
  def currencyUnitsUpdated(self):
    """
    Returns bool.
    """
    return not self.currency_units is None
  
  def toDocument(self):
    """
    Returns dict.
    Raises RuntimeError.
    """
    try:
      result = {
        "company_acronym": self.company_acronym,
        "currency_units": self.currency_units,
        "date": self.date.strftime(FinancialReport.date_format),
        "measurements": self.measurements
      }
      return result
    except Exception as err:
      err_msg = "%s -- toDocument -- Failed.\n%s" % (
        FinancialReport.class_name,
        format_exc(FinancialReport.max_error_chars, err)
      )
      raise RuntimeError(err_msg)
   
  def _getFinancialIndicatorsRegEx(self):
    """
    Returns dict.
    It is a JSON with configurations which maps financial indicator to ReGex.
    Raises RuntimeError.
    """
    result = dict()
    
    try:
      path_to_config = join(dirname(__file__), "%s.json" % "financial_indicators")
      if exists(path_to_config):
        with open(path_to_config, "r") as read_file:
          result = load(read_file)
          read_file.close()
    except Exception as err:
      err_msg = "%s -- _getFinancialIndicatorsRegEx -- Failed to read from the configuration file\nfile_path:\t %s" % (
        self._class_name, format_exc(FinancialReport.max_err_chars, err)
      )
      raise RuntimeError(err_msg)
    
    return result
  
  def __str__(self):
    """
    Returns str.
    Raises RuntimeError.
    """
    return str(self.toDocument())

  # Financial indicators

  def availableCash(self):
    """
    Returns float or None.
    Raises RuntimeError.
    """
    try:
      result = None
      
      if not "cash" in self._regex:
        raise RuntimeError("Expected regex for the indicator cash")
      
      for pattern in self._regex["cash"]:
        
        for measurement in self.measurements.keys():
          match_obj = match(pattern, measurement)
          
          if match_obj:
            wanted_value = self.measurements[match_obj[0]]
            result = float(wanted_value)
            break
        
        if result:
          break
    
      return result
    except RuntimeError as err:
      err_msg = "%s -- availableCash -- Failed.\n%s" % (FinancialReport.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- availableCash -- Failed.\n%s" % (
        FinancialReport.class_name,
        format_exc(FinancialReport.max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def equity(self):
    """
    Returns float or None.
    """
    try:
      result = None
      
      if not "equity" in self._regex:
        raise RuntimeError("Expected regex for the indicator equity")
      
      for pattern in self._regex["equity"]:
        
        for measurement in self.measurements.keys():
          match_obj = match(pattern, measurement)
          
          if match_obj:
            wanted_value = self.measurements[match_obj[0]]
            result = float(wanted_value)
            break
        
        if result:
          break
    
      return result
    except RuntimeError as err:
      err_msg = "%s -- equity -- Failed.\n%s" % (FinancialReport.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- equity -- Failed.\n%s" % (
        FinancialReport.class_name,
        format_exc(FinancialReport.max_error_chars, err)
      )
      raise RuntimeError(err_msg)
  
  def goodwill(self):
    """
    Returns float or None.
    """
    try:
      result = None
      
      if not "goodwill" in self._regex:
        raise RuntimeError("Expected regex for the indicator goodwill")
      
      for pattern in self._regex["goodwill"]:
        
        for measurement in self.measurements.keys():
          match_obj = match(pattern, measurement)
          
          if match_obj:
            wanted_value = self.measurements[match_obj[0]]
            result = float(wanted_value)
            break
        
        if result:
          break
    
      return result
    except RuntimeError as err:
      err_msg = "%s -- goodwill -- Failed.\n%s" % (FinancialReport.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- goodwill -- Failed.\n%s" % (
        FinancialReport.class_name,
        format_exc(FinancialReport.max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def longTermDebt(self):
    """
    Returns float or None.
    """
    try:
      result = None
      
      if not "long_term_debt" in self._regex:
        raise RuntimeError("Expected regex for the indicator long_term_debt")
      
      for pattern in self._regex["long_term_debt"]:
        
        for measurement in self.measurements.keys():
          match_obj = match(pattern, measurement)
          
          if match_obj:
            wanted_value = self.measurements[match_obj[0]]
            result = float(wanted_value)
            break
        
        if result:
          break
    
      return result
    except RuntimeError as err:
      err_msg = "%s -- longTermDebt -- Failed.\n%s" % (FinancialReport.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- longTermDebt -- Failed.\n%s" % (
        FinancialReport.class_name,
        format_exc(FinancialReport.max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def totalAssets(self):
    """
    Returns float or None.
    """
    try:
      result = None
      
      if not "total_assets" in self._regex:
        raise RuntimeError("Expected regex for the indicator total_assets")
      
      for pattern in self._regex["total_assets"]:
        
        for measurement in self.measurements.keys():
          match_obj = match(pattern, measurement)
          
          if match_obj:
            wanted_value = self.measurements[match_obj[0]]
            result = float(wanted_value)
            break
        
        if result:
          break
    
      return result
    except RuntimeError as err:
      err_msg = "%s -- totalAssets -- Failed.\n%s" % (FinancialReport.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- totalAssets -- Failed.\n%s" % (
        FinancialReport.class_name,
        format_exc(FinancialReport.max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def totalLiabilities(self):
    """
    Returns float or None.
    """
    try:
      result = None
      
      if not "total_liabilities" in self._regex:
        raise RuntimeError("Expected regex for the indicator total_liabilities")
      
      for pattern in self._regex["total_liabilities"]:
        
        for measurement in self.measurements.keys():
          match_obj = match(pattern, measurement)
          
          if match_obj:
            wanted_value = self.measurements[match_obj[0]]
            result = float(wanted_value)
            break
        
        if result:
          break
    
      return result
    except RuntimeError as err:
      err_msg = "%s -- totalLiabilities -- Failed.\n%s" % (FinancialReport.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- totalLiabilities -- Failed.\n%s" % (
        FinancialReport.class_name,
        format_exc(FinancialReport.max_error_chars, err)
      )
      raise RuntimeError(err_msg)
  
  # Getters and setters

  @property
  def company_acronym(self):
    """
    Returs str or None.
    """
    return self._company_acronym
  
  @property
  def currency_units(self):
    """
    Returs str or None.
    """
    return self._currency_units

  @property
  def date(self):
    """
    Returns datetime or None.
    """
    return self._date

  @property
  def measurements(self):
    """
    Returns dict.
    """
    return self._measurements

  @company_acronym.setter
  def company_acronym(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      val -- str -- unique identifier of a company at the stock exchange.
    """
    if val and isinstance(val, str):
      self._company_acronym = val
    else:
      raise RuntimeError("%s -- company_acronym -- setter expectes a non-empty str." % FinancialReport.class_name)
  
  @currency_units.setter
  def currency_units(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      val -- str -- currency units, i.e. USD.
    """
    if val and isinstance(val, str):
      self._currency_units = val
    else:
      self._currency_units = "Millions" # TODO: validate during data gathering that missing value is taken from
                                        # most of the reports
      # raise RuntimeError("%s -- currency_units -- setter expectes a non-empty str." % FinancialReport.class_name)

  @date.setter
  def date(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      val -- datetime.
    """
    if val and isinstance(val, datetime):
      self._date = val
    else:
      raise RuntimeError("%s -- date -- setter expectes a datetime object." % FinancialReport.class_name)

  @measurements.setter
  def measurements(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      val -- dict -- maps measurement to the value.
    """
    if val and isinstance(val, dict):
      self._measurements = val
    else:
      raise RuntimeError("%s -- measurements -- setter expectes a non-empty dict" % FinancialReport.class_name)
