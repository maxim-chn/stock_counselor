from datetime import datetime
from logging import getLogger
from traceback import format_exc

from common.applicative_user import ApplicativeUser
from common.backend_tasks.recommendation.task import Progress, Task
from common.database_api import DatabaseApi
from common.financial_report import FinancialReport
from common.financial_user_profile import FinancialIndicators, FinancialUserProfile
from common.investment_recommendation import InvestmentRecommendation
from common.loggable_api import Loggable
from common.recommendation_backend_tasks_api import BackendTasks

max_error_chars = 5000

def startRecommendationWorkerService(service_name):
  """
  Returns void.
  Raises RuntimeError.
  Subscribes to investment recommendation tasks with logic to execute them.
  Arguments:
    service_name -- str.
  """
  def consumeMessagesFromMainService(ch, method, properties, body):
    """
    Returns void.
    Raises RuntimeError.
    Logic for the execution of the investment recommendation calculation.
    Arguments:
      - ch -- Channel -- RabbitMq channel.
      - method -- ???
      - properties -- ???
      - body -- ??? -- contains the message which represents the Task.
    """
    worker = Worker(service_name)
    task = None

    try:
      message = body.decode("utf-8")
      task = Task.fromJson(message)
    except Exception as err:
      err_msg = "%s -- consumeMessagesFromMainService -- Failed to parsed message to Task.\n%s" % (
        service_name,
        format_exc(max_error_chars, err)
      )
      getLogger(service_name).error(err_msg)
      ch.stop_consuming()
      return

    try:
      worker.calculateInvestmentRecommendation(task)
    except RuntimeError as err:
      err_msg = "%s -- consumeMessagesFromMainService -- Failed to execute the Task.\n%s" % (service_name, str(err))
      getLogger(service_name).error(err_msg)

  try:
    backend_tasks = BackendTasks(service_name)
  except RuntimeError as err:
    err_msg = "%s -- startRecommendationWorkerService -- Failed to initiate BackendTasks.\n%s" % (
      service_name,
      str(err)
    )
    raise RuntimeError(err_msg)
  
  try:
    backend_tasks.consumeMessage(consumeMessagesFromMainService)
  except RuntimeError as err:
    err_msg = "%s -- startRecommendationWorkerService -- Failed to subscribe to backend tasks.\n%s" % (
      service_name,
      str(err)
    )
    raise RuntimeError(err_msg)

class Worker(Loggable):
  """
  Reveals an external API for executing the backend tasks related to the investment recommendation calculation.
  """

  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Arguments:
      - service_name -- str.
    """
    super().__init__(service_name, "Worker")
    self._backend_tasks = BackendTasks(service_name)
    self._database = DatabaseApi(service_name)
    self._max_error_chars = max_error_chars
    self._minimum_match_score = 0.7

  def calculateInvestmentRecommendation(self, task):
    """
    Returns void.
    Raises RuntimeError.
    Persists InvestmentRecommendation for a user.
    Arguments:
      task -- Task.
    """
    self._debug("calculateInvestmentRecommendation", "Start\ntask:\t%s" % str(task))

    try:
      task.progress = Progress.RETRIEVING_FINANCIAL_USER_PROFILE
      self._backend_tasks.updateTaskProgressBy(task)

      document = self._database.readApplicativeUserDocumentBy({ "user_id": task.user_id })
      applicative_user = ApplicativeUser.fromDocument(document)
    except RuntimeError as err:
      err_msg = "%s -- calculateInvestmentRecommendation -- Failed to applicative user.\n%s" % (
        self._class_name,
        str(err)
      )
      raise RuntimeError(err_msg)
    
    try:
      task.progress = Progress.RETRIEVING_FINANCIAL_USER_PROFILE
      self._backend_tasks.updateTaskProgressBy(task)

      document = self._database.readFinancialUserProfileDocumentBy({ "user_id": applicative_user.user_id })
      financial_user_profile = FinancialUserProfile.fromDocument(document)
    except RuntimeError as err:
      err_msg = "%s -- calculateInvestmentRecommendation -- Failed to obtain financial user profile.\n%s" % (
        self._class_name,
        str(err)
      )
      raise RuntimeError(err_msg)

    company_acronyms = None
    try:
      task.progress = Progress.RETRIEVING_COMPANY_ACRONYMS_WITH_FINANCIAL_REPORTS
      self._backend_tasks.updateTaskProgressBy(task)

      company_acronyms = self._database.getAcronymsForCompaniesWithFinancialReports()
      
      if not company_acronyms:
        raise RuntimeError("No company with financial reports was found")
    except RuntimeError as err:
      err_msg = "%s -- calculateInvestmentRecommendation.\n%s" % self._class_name
      err_msg += " -- Failed to obtain company acronyms with financial reports.\n%s" % str(err)
      raise RuntimeError(err_msg)

    recommendations_to_calculate = []
    try:
      task.progress = Progress.SUMMARIZING_INVESTMENT_RECOMMENDATIONS_TO_CALCULATE
      self._backend_tasks.updateTaskProgressBy(task)
      
      for company_acronym in company_acronyms:
        investment_recommendation = InvestmentRecommendation()
        investment_recommendation.company_acronym = company_acronym
        investment_recommendation.user_id = applicative_user.user_id
        investment_recommendation.date = datetime.now()
        recommendations_to_calculate.append(investment_recommendation)
    except RuntimeError as err:
      err_msg = "%s -- calculateInvestmentRecommendation." % self._class_name
      err_msg += " -- Failed to summarize InvestmentRecommendations to calculate.\n%s" % str(err)
      raise RuntimeError(err_msg)

    company_acronyms_to_financial_reports = dict()
    try:
      task.progress = Progress.COLLECTING_COMPANIES_FINANCIAL_REPORTS
      self._backend_tasks.updateTaskProgressBy(task)

      for company_acronym in company_acronyms:
        financial_reports = []
        documents = self._database.readFinancialReportDocumentsBy({ "company_acronym": company_acronym })
        for document in documents:
          financial_report = FinancialReport.fromDocument(document)
          financial_reports.append(financial_report)
        
        if not financial_reports:
          self._debug(
            "calculateInvestmentRecommendation",
            "\tExpected financial_reports for the company %s" % company_acronym
          )

        company_acronyms_to_financial_reports[company_acronym] = financial_reports
    except RuntimeError as err:
      err_msg = "%s -- calculateInvestmentRecommendation." % self._class_name
      err_msg += " -- Failed to map company acronyms to FinancialReports.\n%s" % str(err)
      raise RuntimeError(err_msg)
    
    try:
      task.progress = Progress.CALCULATING_SIMILARITY_SCORES
      self._backend_tasks.updateTaskProgressBy(task)
    except RuntimeError as err:
      err_msg = "%s -- calculateInvestmentRecommendation" % self._class_name
      err_msg += " -- Failed to update the Task progress to calculating similarity scores.\n%s" % str(err)
    
    for investment_recommendation in recommendations_to_calculate:
      try:
        financial_reports = company_acronyms_to_financial_reports[investment_recommendation.company_acronym]
        total_similarity_score = self._totalSimilarityScore(financial_reports, financial_user_profile)
        investment_recommendation.similarity_score = total_similarity_score
        self._persistInvestmentRecommendation(investment_recommendation)
      except RuntimeError as err:
        err_msg = "%s -- calculateInvestmentRecommendation" % self._class_name
        err_msg += " -- Failed to calculate total similarity score between user %s" % applicative_user.user_id
        err_msg += " and company %s.\n%s" % (investment_recommendation.company_acronym, str(err))
        raise RuntimeError(err_msg)
    
    try:
      task.progress = Progress.FINISHED
      self._backend_tasks.updateTaskProgressBy(task)
    except RuntimeError as err:
      err_msg = "%s -- calculateInvestmentRecommendation" % self._class_name
      err_msg += " -- Failed to update the Task progress to finished.\n%s" % str(err)

    self._debug("calculateInvestmentRecommendation", "Finish")

  def _idealIndicatorValueForUser(self, rule):
    """
    Returns a float.
    A single user indicator (recommendation preference) can be an acceptable range.
    However, company's financial data is always a precise value.
    Hence, we find an acceptable median for the user indicator which is a single value, as well.
    """
    return (rule["lower_boundary"] + rule["upper_boundary"]) / 2

  def _indicatorCashToLongTermDebt(self, financial_report):
    """
    Returns float.
    It is a ratio between available cash to long term debt.
    Raises RuntimeError.
    Arguments:
      financial_report -- FinancialReport.
    """
    try:
      self._debug("_indicatorCashToLongTermDebt", "Start")
      
      cash = financial_report.availableCash()
      if not cash:
        raise RuntimeError("Expected available cash measurement, got None.")
      
      long_term_debt = financial_report.longTermDebt()
      if not long_term_debt:
        raise RuntimeError("Expected long term debt measurement, got None.")

      if long_term_debt > 0:
        result = cash / long_term_debt
      else:
        result = cash
      
      self._debug("_indicatorCashToLongTermDebt", "Finish\nresult:\t%s" % str(result))
      return result
    except RuntimeError as err:
      err_msg = "%s -- _indicatorCashToLongTermDebt -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def _indicatorEquityToGoodwill(self, financial_report):
    """
    Returns float.
    It is a ratio between equity to goodwill.
    Arguments:
      financial_report -- FinancialReport.
    """
    try:
      self._debug("_indicatorEquityToGoodwill", "Start")
      
      equity = financial_report.equity()
      if not equity:
        total_assets = financial_report.totalAssets()
        if not total_assets:
          raise RuntimeError("Expected total assets measurement, but got None.")

        total_liabilities = financial_report.totalLiabilities()
        if not total_liabilities:
          raise RuntimeError("Expected total liabilities measurement, but got None.")

        equity = total_assets - total_liabilities

      goodwill = financial_report.goodwill()
      if not goodwill:
        raise RuntimeError("Expected goodwill measurement, but got None.")
      
      if goodwill > 0:
        result = equity / goodwill
      else:
        result = equity
      
      self._debug("_indicatorEquityToGoodwill", "Finish\nresult:\t%s" % str(result))
      return result
    except RuntimeError as err:
      err_msg = "%s -- _indicatorEquityToGoodwill -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def _similarityScore(self, financial_report, financial_user_profile):
    """
    Returns a float.
    Raises RuntimeError.
    It is the similarity score in the range of [0, 1].
    0 means the profiles are completely different.
    1 means the profiles are identical.
    Keyword arguments:
      - financial_reports -- list<FinancialReport>.
      - financial_user_profile -- FinancialUserProfile.
    """
    msg = "Start\nfinacial_report:\t%s" % str(financial_report)
    msg += ",\nfinancial_user_profile:\t%s" % str(financial_user_profile)
    self._debug("_similarityScore", msg)

    result = 0
    for indicator in financial_user_profile.rules.keys():
      rule = financial_user_profile.rules[indicator]
      ideal_indicator_value_for_user = self._idealIndicatorValueForUser(rule)
      actual_indicator_value_from_report = None
      
      if indicator == FinancialIndicators.CASH_TO_LONG_TERM_DEBT.value:
        actual_indicator_value_from_report = self._indicatorCashToLongTermDebt(financial_report)
      elif indicator == FinancialIndicators.EQUITY_TO_GOODWILL.value:
        actual_indicator_value_from_report = self._indicatorEquityToGoodwill(financial_report)
      else:
        err_msg = "%s -- _similarityScore -- Failed to calclulate actual indicator \"%s\" value" % (self._class_name, indicator)
        raise RuntimeError(err_msg)
      
      difference = ideal_indicator_value_for_user - actual_indicator_value_from_report
      normalized_difference = abs(difference / max([
        ideal_indicator_value_for_user,
        actual_indicator_value_from_report
      ]))
      result += rule["weight"] * normalized_difference / financial_user_profile.rulesCount()
    
    self._debug("_similarityScore", "Finish\nresult:\t%.2f" % result)
    return result
  
  def _persistInvestmentRecommendation(self, investment_recommendation):
    """
    Returns void.
    Raises RuntimeError.
      - investment_recommendation -- InvestmentRecommendation.
    """
    try:
      self._debug("_persistInvestmentRecommendation", "Start\ninvestment_recommendation:\t%s" % str(investment_recommendation))
      self._database.createInvestmentRecommendationDocument(investment_recommendation.toDocument())
      self._debug("_persistInvestmentRecommendation", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- _persistInvestmentRecommendation -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def _totalSimilarityScore(self, financial_reports, financial_user_profile):
    """
    Returns a float.
    Raises RuntimeError.
    It is the similarity score in the range of [0, 1].
    0 means the profiles are completely different.
    1 means the profiles are identical.
    Keyword arguments:
      - financial_reports -- list<FinancialReport>.
      - financial_user_profile -- FinancialUserProfile.
    """
    msg = "Start\nfinacial_reports:\tavailable for %d years" % len(financial_reports)
    msg += ",\nfinancial_user_profile:\t%s" % financial_user_profile
    self._debug("_totalSimilarityScore", msg)
    
    result = 0
    for financial_report in financial_reports:
      score = self._similarityScore(financial_report, financial_user_profile)
      result += score / len(financial_reports)
    
    self._debug("_totalSimilarityScore", "Finish\nresult:\t%.2f" % result)
    return result
