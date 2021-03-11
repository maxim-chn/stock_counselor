from backend_tasks_api import BackendTasksApi
from common_classes.loggable import Loggable
from model_api import ModelApi
from os import path
from json import dumps, load
from re import search


class WorkerApi(Loggable):
  def __init__(self):
    super().__init__("WorkerApi")
    self._model = ModelApi()
    self._backend_tasks = BackendTasksApi()
    self._financial_keys_regex = self._loadFinancialKeysRegex()
    self._minimum_match_score = 0.7
    self._gen_to_csim_ratio = 0.5

  def getUserIdForGathering(self):
    self._debug("getUserIdForGathering", "Start")
    result = self._backend_tasks.getUserIdOfTaskWithProgressInitiated()
    self._debug("getUserIdForGathering", "Finish - result: %s\n" % result)
    return result

  def calculateRecommendationByUserId(self, user_id):
    result = []
    user_profile = self._model.getUserProfileByUserId(user_id)
    print(user_profile)
    companies_financial_data = self._model.getCompaniesFinancialData()
    for company_financial_data in companies_financial_data:
      company_profiles = self._companyProfilesFromFinancialData(company_financial_data)
      print(company_profiles)
      if self._areSimilarProfiles(user_profile, company_profiles):
        result.append(company_financial_data["acronym"])

    return result

  def _indicatorValueFromUserProfile(self, indicator):
    return (indicator["lower_boundary"] + indicator["upper_boundary"]) / 2

  def _areSimilarProfiles(self, user_profile, company_profiles):
    for date_str, company_profile in company_profiles.items():
      print("Calculating similarity for %s" % (date_str))
      score = self._calculateContentSimilariy(user_profile, company_profile)
      print("Score is %f" % (score))
      if score < self._minimum_match_score:
        return False
    return True

  def _calculateContentSimilariy(self, user_profile, company_profile):
    result = 0
    indicators_count = len(user_profile.keys())
    for indicator_key, indicator_data in user_profile.items():
      diff = (self._indicatorValueFromUserProfile(indicator_data) - company_profile[indicator_key]) / max([
        self._indicatorValueFromUserProfile(indicator_data),
        company_profile[indicator_key]
      ])
      result += indicator_data["weight"] * abs(diff) / indicators_count
    return result

  def _calculateCashToLongTermDebt(self, company_profile):
    for date_str in company_profile.keys():
      cash = float(company_profile[date_str]["cash"])
      long_term_debt = float(company_profile[date_str]["long_term_debt"])
      if long_term_debt > 0:
        company_profile[date_str]["cash_to_long_term_debt"] = cash / long_term_debt
      else:
        company_profile[date_str]["cash_to_long_term_debt"] = cash

  def _calculateEquityToGoodwill(self, company_profile):
    for date_str in company_profile.keys():
      equity = float(company_profile[date_str]["total_assets"]) - float(company_profile[date_str]["total_liabilities"])
      goodwill = float(company_profile[date_str]["goodwill"])
      if goodwill > 0:
        company_profile[date_str]["equity_to_goodwill"] = equity / goodwill
      else:
        company_profile[date_str]["equity_to_goodwill"] = equity

  def _companyProfilesFromFinancialData(self, company_financial_data):
    result = dict()
    for date_str, financial_data_from_source in company_financial_data["data"].items():
      result[date_str] = dict()
      for financial_key_for_profile, regex_for_key_in_source in self._financial_keys_regex.items():
        for financial_key_in_source, financial_value in financial_data_from_source["data"].items():
          search_obj = search(regex_for_key_in_source, financial_key_in_source.lower())
          if search_obj:
            result[date_str][financial_key_for_profile] = financial_value
            break
    self._calculateEquityToGoodwill(result)
    self._calculateCashToLongTermDebt(result)
    result = self._removeNonIndicators(result)
    return result

  def _loadFinancialKeysRegex(self):
    result = None
    file_path = path.join(
      path.dirname(__file__),
      "worker",
      "financial_values_regex.json"
    )
    with open(file_path, "r") as read_file:
      result = load(read_file)
    return result

  def _removeNonIndicators(self, company_profile):
    result = dict()
    for date_str in company_profile.keys():
      result[date_str] = dict()
      for key, value in company_profile[date_str].items():
        if "_to_" in key:
          result[date_str][key] = value
    return result