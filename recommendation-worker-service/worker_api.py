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

  def getUserIdForGathering(self):
    self._debug("getUserIdForGathering", "Start")
    result = self._backend_tasks.getUserIdOfTaskWithProgressInitiated()
    self._debug("getUserIdForGathering", "Finish - result: %s\n" % result)
    return result

  def calculateRecommendationByUserId(self, user_id):
    result = []
    user_profile = self._model.getUserProfileByUserId(user_id)
    print(user_profile)
    exit(0)
    companies_financial_data = self._model.getCompaniesFinancialData()
    for company_financial_data in companies_financial_data:
      company_profile = self._companyProfileFromFinancialData(company_financial_data)
      print(company_profile)
      profiles_match_score = self._calculateSimilarity(company_profile, user_profile)
      if profiles_match_score >= self._minimum_match_score:
        result.append(company_profile["acronym"])

    return result


  def _companyProfileFromFinancialData(self, company_financial_data):
    company_acronym = company_financial_data["acronym"]
    result = {
      company_acronym: dict()
    }
    for date_str, financial_data_from_source in company_financial_data["data"].items():
      result[company_acronym][date_str] = dict()
      for financial_key_for_profile, regex_for_key_in_source in self._financial_keys_regex.items():
        for financial_key_in_source, financial_value in financial_data_from_source["data"].items():
          search_obj = search(regex_for_key_in_source, financial_key_in_source.lower())
          if search_obj:
            result[company_acronym][date_str][financial_key_for_profile] = financial_value
            break
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
