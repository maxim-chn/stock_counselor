from datetime import datetime
from json import dumps
from traceback import format_exc

class InvestmentRecommendation:
  """
  Represents an investment recommendation for a user.
  """
  class_name = "InvestmentRecommendation"
  date_format = '%Y-%m-%d'
  max_error_chars = 1000

  def __init__(self):
    self._company_acronym = None
    self._date = None
    self._similarity_score = None
    self._user_id = None

  @classmethod
  def investmentRecommendationWith(cls, company_acronym, date, similarity_score, user_id):
    """
    Returns InvestmentRecommendation.
    Raises RuntimeError.
    Arguments:
      company_acronym -- str -- unique identifier of a company at the stock exchange.
      date -- datetime.
      similariy_score -- float.
      user_id -- str -- unique user id at the database.
    """
    try:
      result = cls()
      result.company_acronym = company_acronym
      result.date = date
      result.similarity_score = similarity_score
      result.user_id = user_id
      return result
    except RuntimeError as err:
      err_msg = "%s -- investmentRecommendationWith -- Failed.\n%s" % (InvestmentRecommendation.class_name, str(err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromDocument(cls, val):
    """
    Returns InvestmentRecommendation.
    Raises RuntimeError.
    Arguments:
      val -- dict -- Document which represents InvestmentRecommendation.
    """
    try:
      company_acronym = val["company_acronym"]
      date = datetime.strptime(val["date"], InvestmentRecommendation.date_format)
      similarity_score = float(val["similarity_score"])
      user_id = val["user_id"]
      result = cls.investmentRecommendationWith(company_acronym, date, similarity_score, user_id)
      return result
    except RuntimeError as err:
      err_msg = "%s -- fromDocument -- Failed.\n%s" % (InvestmentRecommendation.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- fromDocument -- Failed.\n%s" % (
        InvestmentRecommendation.class_name, format_exc(InvestmentRecommendation.max_error_chars, err)
      )

  def toDocument(self):
    """
    Returns dict.
    Raises RuntimeError.
    """
    try:
      result = {
        "company_acronym": self.company_acronym,
        "date": self.date.strftime(InvestmentRecommendation.date_format),
        "similarity_score": str(self.similarity_score),
        "user_id": self.user_id
      }
      return result
    except Exception as err:
      err_msg = "%s -- toDocument -- Failed.\n%s" % (
        InvestmentRecommendation.class_name, format_exc(InvestmentRecommendation.max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def toJson(self):
    """
    Returns str.
    Raises RuntimeError.
    """
    try:
      asDocument = self.toDocument()
      return dumps(asDocument)
    except RuntimeError as err:
      err_msg = "%s -- toJson -- Failed.\n%s" % (InvestmentRecommendation.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- toJson -- Failed.\n%s" % (
        InvestmentRecommendation.class_name,
        format_exc(InvestmentRecommendation.max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def __str__(self):
    """
    Returns str.
    Raises RuntimeError.
    """
    return str(self.toDocument())

  # Getters and setters

  @property
  def company_acronym(self):
    """
    Returns str or None.
    """
    return self._company_acronym

  @property
  def date(self):
    """
    Returns datetime or None.
    """
    return self._date

  @property
  def similarity_score(self):
    """
    Returns float or None.
    """
    return self._similarity_score

  @property
  def user_id(self):
    """
    Returns str or None.
    """
    return self._user_id

  @company_acronym.setter
  def company_acronym(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      val -- str.
    """
    if val and isinstance(val, str):
      self._company_acronym = val
    else:
      err_msg = "%s -- company_acronym -- setter expects a non-empty str." % InvestmentRecommendation.class_name
      raise RuntimeError(err_msg)

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
      raise RuntimeError("%s -- date -- setter expectes a datetime object." % InvestmentRecommendation.class_name)

  @similarity_score.setter
  def similarity_score(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      val -- float.
    """
    if val and isinstance(val, float) and val >= 0 and val <= 1:
      self._similarity_score = val
    else:
      err_msg = "%s -- similarity_score" % InvestmentRecommendation.class_name
      err_msg += " -- setter expectes a float between [0, 1]."
      raise RuntimeError(err_msg)
  
  @user_id.setter
  def user_id(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      val -- str -- unique user id at the database.
    """
    if val and isinstance(val, str) and "@" in val and "." in val:
      self._user_id = val
    else:
      raise RuntimeError("%s -- user_id -- setter expected an email address." % InvestmentRecommendation.class_name)
