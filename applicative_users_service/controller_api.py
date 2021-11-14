from applicative_users_service.invalid_credentials_error import InvalidCredentialsError

from common.applicative_user import ApplicativeUser
from common.database_api import DatabaseApi
from common.financial_user_profile import FinancialUserProfile
from common.loggable_api import Loggable
from common.portfolio_risk_level import PortfolioRiskLevel

class Controller(Loggable):
  """
  This is our Controller Logic which reveals an API for the Boundary.
  The available methods connect between an input from the Boundary and the database.
  """

  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Arguments:
      service_name -- str.
    """
    super().__init__(service_name, "Controller")
    self._database = DatabaseApi(service_name)

  def getExistingUserBy(self, email, first_name, last_name):
    """
    Returns str.
    It represents the ApplicativeUser.
    Raises InvalidCredentialsError or RuntimeError.
    Arguments:
      email -- str.
      first_name -- str.
      last_name -- str.
    """
    function_name = "getExistingUserBy"
    self._debug(function_name, "Start\nemail:\t%s\nfirst_name:\t%s\nlast_name:\t%s" % (email, first_name, last_name))
    
    if not self._isEmailLegal(email):
      raise InvalidCredentialsError("Email is illegal")
    if not self._isFirstNameLegal(first_name):
      raise InvalidCredentialsError("First name is illegal")
    if not self._isLastNameLegal(last_name):
      raise InvalidCredentialsError("Last name is illegal")
    
    try:
      existing_user_as_document = self._database.readApplicativeUserDocumentBy({ "user_id": email })
      
      if existing_user_as_document and isinstance(existing_user_as_document, dict):
        result = ApplicativeUser.fromDocument(existing_user_as_document).toJson()
        self._debug(function_name, "Finish\nresult:\t%s" % str(result))
        return result
      
      raise RuntimeError("Provided credentials have matched no existing user")
    except RuntimeError as err:
      error_msg = "%s -- %s -- Failed.\n%s" % (self._class_name, function_name, str(err))
      raise RuntimeError(error_msg)


  def newUserBy(self, email, first_name, last_name, portfolio_risk_level):
    """
    Returns str.
    It represents the ApplicativeUser.
    Raises InvalidCredentialsError or RuntimeError.
    Arguments:
      email -- str.
      first_name -- str.
      last_name -- str.
      portfolio_risk_level -- PortfolioRiskLevel.
    """
    function_name = "newUserBy"
    self._debug(function_name, "Start:\nemail:\t%s\nfirst_name:\t%s\nlast_name:\t%s\nportfolio_risk_level:\t%s" % (
      email,
      first_name,
      last_name,
      str(portfolio_risk_level)
    ))
    
    if not self._isEmailLegal(email):
      raise InvalidCredentialsError("Email is illegal")
    if not self._isFirstNameLegal(first_name):
      raise InvalidCredentialsError("First name is illegal")
    if not self._isLastNameLegal(last_name):
      raise InvalidCredentialsError("Last name is illegal")
    if not self._isPortfolioRiskLevelLegal(portfolio_risk_level):
      raise InvalidCredentialsError("Portfolio risk level is illegal")
    
    try:
      
      if self._database.doesApplicativeUserDocumentExist({"user_id": email }):
        raise RuntimeError("Provided credentials match an existing user")
      
      new_user = ApplicativeUser.applicativeUserWith(first_name, last_name, email)
      financial_user_profile = FinancialUserProfile.fromPortfolioRiskLevel(portfolio_risk_level, new_user.user_id)
      self._database.createFinancialUserProfileDocument(financial_user_profile.toDocument())
      self._database.createApplicativeUserDocument(new_user.toDocument())
      existing_user_as_document = self._database.readApplicativeUserDocumentBy({ "user_id": email })
      result = ApplicativeUser.fromDocument(existing_user_as_document).toJson()

      self._debug(function_name, "Finish\nresult:\t%s" % str(result))
      return result
    except RuntimeError as err:
      error_msg = "%s -- %s -- Failed.\n%s" % (self._class_name, "newUserBy", str(err))
      raise RuntimeError(error_msg)

  def _isEmailLegal(self, val):
    """
    Returns bool.
    Arguments:
      val -- str.
    """
    if val and isinstance(val, str) and "@" in val and "." in val:
      return True
    return False

  def _isFirstNameLegal(self, val):
    """
    Returns bool.
    Arguments:
      val -- str.
    """
    if val and isinstance(val, str) and len(val) > InvalidCredentialsError.MIN_FIRST_NAME_LENGTH:
      return True
    return False

  def _isLastNameLegal(self, val):
    """
    Returns bool.
    Arguments:
      val -- str.
    """
    if val and isinstance(val, str) and len(val) > InvalidCredentialsError.MIN_LAST_NAME_LENGTH:
      return True
    return False

  def _isPortfolioRiskLevelLegal(self, val):
    """
    Returns bool.
    Arguments:
      val -- str.
    """
    if val and isinstance(val, PortfolioRiskLevel):
      return True
    return False      
