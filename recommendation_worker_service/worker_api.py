from common.loggable_api import Loggable
from enum import Enum
from json import load
from logging import getLogger, DEBUG, FileHandler, Formatter
from os import path
from re import search
from recommendation_worker_service.backend_tasks_api import BackendTasks
from recommendation_worker_service.entity_api import Entity
from time import sleep

class CalculationProgress(Enum):
  COMPARING_USER_AND_COMPANY_PROFILES = "Checking if User Profile matches that of the Company"
  CREATING_COMPANY_PROFILE = "Creating Company Financial Profile from the Financial Data"
  READING_COMPANY_FINANCIAL_DATA = "Reading the Company Financial Data"
  READING_USER_PROFILE = "Reading the User Investment Recommendations"

class Worker(Loggable):
  """
  Reveals an external API for executing the backend tasks related to the investment recommendation calculation.
  """

  def __init__(self):
    super().__init__("recommendation_worker_service", "Worker")
    self._log_id = "recommendation_worker_service"
    self._backend_tasks = BackendTasks(self._log_id)
    self._entity = Entity(self._log_id)
    self._financial_keys_regex = self._loadFinancialKeysRegex()
    self._minimum_match_score = 0.7

  def startRecommendationWorkerService(self):
    self._setupLogger()
    while True:
      user_id = self._getUserIdForInvestmentRecommendationCalculation()

      if user_id is None:
        sleep(5)
        continue

      recommendation = self._calculateRecommendationByUserId(user_id)
      self._entity.storeRecommendation(recommendation)

  def _areSimilarProfiles(self, user_profile, company_profiles):
    """
    Returns a bool.
    Keyword arguments:
      company_profiles -- dict -- contains the financial data of a company per calendar year.
      user_profile -- dict -- the financial indicators that represent investment preferences.
    """
    self._debug("_areSimilarProfiles", "Start")
    for date_str, company_profile in company_profiles.items():
      score = self._calculateContentSimilariy(user_profile, company_profile)
      if score < self._minimum_match_score:
        self._debug("_areSimilarProfiles", "Finish - profiles are not similar")
        return False
    self._debug("_areSimilarProfiles", "Finish - profiles are similar")
    return True

  def _calculateCashToLongTermDebt(self, company_profiles):
    """
    Inserts Cash-to-Long-Term-Debt Financial Indicator into the company profiles.
    Keyword arguments:
      company_profiles -- dict -- contains the financial data of a company per calendar year.
    """
    self._debug("_calculateCashToLongTermDebt", "Start")
    for date_str in company_profiles.keys():
      cash = float(company_profiles[date_str]["cash"])
      long_term_debt = float(company_profiles[date_str]["long_term_debt"])
      if long_term_debt > 0:
        company_profiles[date_str]["cash_to_long_term_debt"] = cash / long_term_debt
      else:
        company_profiles[date_str]["cash_to_long_term_debt"] = cash
    self._debug("_calculateCashToLongTermDebt", "Finish")

  def _calculateContentSimilariy(self, user_profile, company_profile):
    """
    Returns a float.
    It is the similarity score in the range of [0, 1].
    0 means the profiles are completely different.
    1 means the profiles are identical.
    Keyword arguments:
      company_profiles -- dict -- contains the financial data of a company per calendar year.
      user_profile -- dict -- the financial indicators that represent investment preferences.
    """
    self._debug("_calculateContentSimilariy", "Start")
    result = 0
    indicators_count = len(user_profile.keys())
    for indicator_key, indicator_data in user_profile.items():
      user_indicator_val = self._indicatorValueFromUserProfile(indicator_data)
      company_indicator_val = company_profile[indicator_key]
      difference = user_indicator_val - company_indicator_val
      normalized_difference = abs(difference / max([user_indicator_val, company_indicator_val]))
      result += indicator_data["weight"] * normalized_difference / indicators_count
    self._debug("_calculateContentSimilariy", "Finish - result: %.2f" % result)
    return result

  def _calculateEquityToGoodwill(self, company_profiles):
    """
    Inserts Equity-to-Goodwill Financial Indicator into the company profiles.
    Keyword arguments:
      company_profiles -- dict -- contains the financial data of a company per calendar year.
    """
    self._debug("_calculateEquityToGoodwill", "Start")
    for date_str in company_profiles.keys():
      total_assets = float(company_profiles[date_str]["total_assets"])
      total_liabilities = float(company_profiles[date_str]["total_liabilities"])
      equity = total_assets - total_liabilities
      goodwill = float(company_profiles[date_str]["goodwill"])
      if goodwill > 0:
        company_profiles[date_str]["equity_to_goodwill"] = equity / goodwill
      else:
        company_profiles[date_str]["equity_to_goodwill"] = equity
    self._debug("_calculateEquityToGoodwill", "Finish")

  def _companyProfilesFromFinancialData(self, company_financial_data):
    """
    Returns a dict.
    It contains the company financial profiles per each calendar year.
    Keyword arguments:
      company_financial_data -- dict -- the persisted financial data of a company from an external source.
    """
    self._debug("_companyProfilesFromFinancialData", "Start")
    result = dict()
    for date_str, financial_data_from_source in company_financial_data["data"].items():
      result[date_str] = dict()
      for financial_key_for_profile, regex_for_financial_key_in_source in self._financial_keys_regex.items():
        for financial_key_in_source, financial_value in financial_data_from_source.items():
          search_obj = search(regex_for_financial_key_in_source, financial_key_in_source.lower())
          if search_obj:
            result[date_str][financial_key_for_profile] = financial_value
            break
    self._calculateCashToLongTermDebt(result)
    self._calculateEquityToGoodwill(result)
    result = self._removeNonIndicators(result)
    self._debug("_companyProfilesFromFinancialData", "Finish - result: %s" % result)
    return result

  def _calculateRecommendationByUserId(self, user_id):
    """
    Returns a dict.
    It holds the recommended stock symbols that represent the companies for the user to invest into.
    Keyword arguments:
      user_id -- str -- an unique identifier of a user inside our program.
    """
    self._debug("_calculateRecommendationByUserId", "Start - user_id: %s" % user_id)
    result = {
      "user_id": user_id,
      "companies": []
    }
    self._backend_tasks.updateTaskByUserId(user_id, CalculationProgress.READING_USER_PROFILE.value)
    user_profile = self._entity.getUserProfileByUserId(user_id)
    self._backend_tasks.updateTaskByUserId(user_id, CalculationProgress.READING_COMPANY_FINANCIAL_DATA.value)
    companies_financial_data = self._entity.getCompaniesFinancialData()
    for company_financial_data in companies_financial_data:
      self._backend_tasks.updateTaskByUserId(user_id, CalculationProgress.CREATING_COMPANY_PROFILE.value)
      company_profiles = self._companyProfilesFromFinancialData(company_financial_data)
      self._backend_tasks.updateTaskByUserId(user_id, CalculationProgress.COMPARING_USER_AND_COMPANY_PROFILES.value)
      if self._areSimilarProfiles(user_profile, company_profiles):
        result["companies"].append(company_financial_data["acronym"])
    self._debug("_calculateRecommendationByUserId", "Finish - result: %s\n" % result)
    return result

  def _getUserIdForInvestmentRecommendationCalculation(self):
    """
    Returns a str.
    It is the unique id of the user in our program.
    """
    self._debug("_getUserIdForInvestmentRecommendationCalculation", "Start")
    result = self._backend_tasks.getUserIdFromNewTask()
    self._debug("_getUserIdForInvestmentRecommendationCalculation", "Finish - result: %s\n" % result)
    return result

  def _indicatorValueFromUserProfile(self, indicator):
    """
    Returns a float.
    A single user indicator (recommendation preference) can be an acceptable range.
    However, company's financial data is always a precise value.
    Hence, we find an acceptable median for the user indicator which is a single value, as well.
    """
    return (indicator["lower_boundary"] + indicator["upper_boundary"]) / 2

  def _loadFinancialKeysRegex(self):
    """
    Returns a dict.
    It contains the Regular Expressions for filtering the company's profile from the financial values
    that are not used for the financial indicator calculations.
    """
    file_path = path.join(
      path.dirname(__file__),
      "worker",
      "financial_values_regex.json"
    )
    with open(file_path, "r") as read_file:
      result = load(read_file)
    return result

  def _removeNonIndicators(self, company_profiles):
    """
    Returns a dict.
    It contains the Financial Indicators for a company per calendar years.
    Keyword arguments:
      company_profiles -- dict -- contains the financial data of a company per calendar year.
    """
    result = dict()
    for date_str in company_profiles.keys():
      result[date_str] = dict()
      for key, value in company_profiles[date_str].items():
        if "_to_" in key:
          result[date_str][key] = value
    return result

  def _setupLogger(self):
    logger = getLogger(self._log_id)
    logger.setLevel(DEBUG)
    file_handler = FileHandler("%s.log" % self._log_id)
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(Formatter("%(msg)s"))
    logger.addHandler(file_handler)