from enum import Enum
from traceback import format_exc

from common.portfolio_risk_level import PortfolioRiskLevel

class FinancialIndicators(Enum):
  CASH_TO_LONG_TERM_DEBT = "cash_to_long_term_debt"
  EQUITY_TO_GOODWILL = "equity_to_goodwill"

class FinancialUserProfile:
  """
  Represents the rules by which financial company reports should be filtered when creating investment recommendations
  for a user.
  """
  class_name = "FinancialUserProfile"
  max_err_chars = 1000

  def __init__(self):
    self._rules = dict()
    self._user_id = None

  @classmethod
  def financialUserProfileWith(cls, rules, user_id):
    """
    Returns FinancialUserProfile.
    Raises RuntimeError.
    Arguments:
      - rules -- dict -- Rules for filtering FinancialReport.
      - user_id -- str -- Email address.
    """
    try:
      result = cls()
      result.rules = rules
      result.user_id = user_id
      return result
    except RuntimeError as err:
      err_msg = "%s -- financialUserProfileWith -- Failed.\n%s" % (FinancialUserProfile.class_name, str(err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromDocument(cls, val):
    """
    Returns FinancialUserProfile.
    Raises RuntimeError.
    Arguments:
      - val -- dict -- Document which represents FinancialUserProfile.
    """
    try:
      rules = val["rules"]
      user_id = val["user_id"]
      result = FinancialUserProfile.financialUserProfileWith(rules, user_id)
      return result
    except RuntimeError as err:
      err_msg = "%s -- fromDocument -- Failed.\n%s" % (FinancialUserProfile.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- fromDocument -- Failed.\n%s" % (
        FinancialUserProfile.class_name, format_exc(FinancialUserProfile.max_err_chars, err)
      )
      raise RuntimeError(err_msg)

  @classmethod
  def fromPortfolioRiskLevel(cls, risk_level, user_id):
    """
    Returns FinancialUserProfile.
    Raises RuntimeError.
    Arguments:
      - risk_level -- PortfolioRiskLevel.
      - user_id -- str -- Email address.
    """
    try:
      if not isinstance(risk_level, PortfolioRiskLevel):
        raise RuntimeError("Unexpected portfolio risk level value")
      result = cls()
      result.user_id = user_id
      if risk_level == PortfolioRiskLevel.LOW:
        result.rules = {
          "cash_to_long_term_debt": {
            "lower_boundary": 10,
            "upper_boundary": 30,
            "weight": 0.7
          },
          "equity_to_goodwill": {
            "lower_boundary": 30,
            "upper_boundary": 100,
            "weight": 1
          }
        }
      elif risk_level == PortfolioRiskLevel.HIGH:
        result.rules = {
          "cash_to_long_term_debt": {
            "lower_boundary": 10,
            "upper_boundary": 70,
            "weight": 0.7
          },
          "equity_to_goodwill": {
            "lower_boundary": 0,
            "upper_boundary": 100,
            "weight": 1
          }
        }
      else:
        raise RuntimeError("Unsupported portfolio risk level")
      return result
    except RuntimeError as err:
      err_msg = "%s -- %s -- Failed.\n%s" % (FinancialUserProfile.class_name, "fromPortfolioRiskLevel", str(err))
      raise RuntimeError(err_msg)
  
  def rulesCount(self):
    if self.rules:
      return len(self.rules)
    else:
      return 0

  def toDocument(self):
    """
    Returns dict.
    """
    result = {
      "rules": self.rules,
      "user_id": self.user_id
    }
    return result

  def __str__(self):
    """
    Returns str.
    """
    return str(self.toDocument())

  # Getters and setters

  @property
  def rules(self):
    """
    Returns dict.
    """
    return self._rules

  @property
  def user_id(self):
    """
    Returns str or None.
    """
    return self._user_id

  @rules.setter
  def rules(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - val -- dict -- Rules for filtering throught the FinancialReport.
    """
    if val and isinstance(val, dict):
      self._rules = val
    else:
      raise RuntimeError("%s -- rules -- setter expected a non empty dictionary" % FinancialUserProfile.class_name)

  @user_id.setter
  def user_id(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - val -- str -- Email address.
    """
    if val and isinstance(val, str) and "@" in val and "." in val:
      self._user_id = val
    else:
      raise RuntimeError("%s -- user_id -- setter expected an email address." % FinancialUserProfile.class_name)
