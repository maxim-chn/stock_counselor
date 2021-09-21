from datetime import datetime
from logging import getLogger
from time import sleep
from traceback import format_exc

from common.data_gathering_backend_tasks_api import BackendTasks
from common.backend_tasks.data_gathering.task import Progress, Task
from common.database_api import DatabaseApi
from common.financial_report import FinancialReport
from common.loggable_api import Loggable
from data_gathering_worker_service.sec_communicator_api import SecCommunicator

max_error_chars = 5000

def startDataGatheringWorkerService(service_name):
  """
  Returns void.
  Raises RuntimeError.
  Subscribes to financial data gathering tasks with logic to execute them.
  Arguments:
    service_name -- str.
  """
  def consumeMessagesFromMainService(ch, method, properties, body):
    """
    Returns void.
    Raises RuntimeError.
    Logic for the execution of the financial data gathering task.
    Arguments:
      - ch -- Channel -- RabbitMq channel.
      - method -- ??? -- ???
      - properties -- ??? -- ???
      - body -- ??? -- contains the message which represents the Task.
    """
    worker = Worker(service_name)
    task = None
    
    try:
      published_message = body.decode("utf-8")
      task = Task.fromJson(published_message)
    except Exception as err:
      ch.stop_consuming()
      err_msg = "%s -- consumeMessagesFromMainService -- Failed.\n%s" % (
        service_name,
        format_exc(max_error_chars, err)
      )
      getLogger(service_name).error(err_msg)

    try:
      worker.gatherFinancialData(task)
    except RuntimeError as err:
      ch.stop_consuming()
      err_msg = "%s -- consumeMessagesFromMainService -- Failed to execute the Task.\n%s" % (
        service_name,
        str(err)
      )
      getLogger(service_name).error(err_msg)
  
  try:
    backend_tasks = BackendTasks(service_name)
  except RuntimeError as err:
    err_msg = "%s -- startDataGatheringWorkerService -- Failed to initiate BackendTasks.\n%s" % (
      service_name,
      str(err)
    )
    raise RuntimeError(err_msg)
  
  try:
    backend_tasks.consumeMessage(consumeMessagesFromMainService)
  except RuntimeError as err:
    err_msg = "%s -- startDataGatheringWorkerService -- Failed to subscribe to backend tasks.\n%s" % (
      service_name,
      str(err)
    )
    raise RuntimeError(err_msg)

class Worker(Loggable):
  """
  Reveals an external API for executing the backend tasks related to the financial data gathering.
  """

  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Arguments:
      service_name -- str.
    """
    super().__init__(service_name, "Worker")
    self._backend_tasks = BackendTasks(service_name)
    self._database = DatabaseApi(service_name)
    self._date_format = '%Y-%m-%d'
    self._farthest_date_relevant = datetime.strptime("2015-01-01", '%Y-%m-%d')
    self._sec_communicator = SecCommunicator(service_name)

  def gatherFinancialData(self, task):
    """
    Returns void.
    Raises RuntimeError.
    Collects financial data and stores it in the database.
    Keyword arguments:
      - task -- Task -- represents a backend task for financial data gathering.
    """
    self._debug("gatherFinancialData", "Start\ntask:\t%s" % str(task))
    financial_reports = []
    
    company_id = None
    try:
      task.progress = Progress.QUERYING_FOR_COMPANY_ID
      self._backend_tasks.updateTaskProgressBy(task)
      company_id = self._sec_communicator.getCompanyId(task.company_acronym)
      
      if not company_id:
        raise RuntimeError("Expected to get Company id, but got None")
    except RuntimeError as err:
      err_msg = "%s -- gatherFinancialData -- Failed to obtain Company id.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

    html_with_10k_search_results = None
    try:
      task.progress = Progress.QUERYING_FOR_AVAILABLE_10K_REPORTS
      self._backend_tasks.updateTaskProgressBy(task)
      sleep(1)
      html_with_10k_search_results = self._sec_communicator.get10kReportsSearchResults(company_id)

      if not html_with_10k_search_results:
        raise RuntimeError("Expected to get Html with 10K Search Results, but got None")
    except RuntimeError as err:
      err_msg = "%s -- gatherFinancialData -- Failed to obtain Html with 10K Search Results.\n%s" % (
        self._class_name,
        str(err)
      )
      raise RuntimeError(err_msg)
    
    accession_numbers = None
    try:
      task.progress = Progress.QUERYING_FOR_10K_IDS
      self._backend_tasks.updateTaskProgressBy(task)
      sleep(1)
      accession_numbers = self._sec_communicator.get10kAccessionNumbers(html_with_10k_search_results)

      if not accession_numbers:
        raise RuntimeError("Expected to get mapping of years to accession numbers, but got empty dict")
    except RuntimeError as err:
      err_msg = "%s -- gatherFinancialData -- Failed to obtain mapping of years to Accession numbers.\n%s" % (
        self._class_name,
        str(err)
      )
      raise RuntimeError(err_msg)

    for date_str, accession_number in accession_numbers.items():
      next_date = datetime.strptime(date_str, self._date_format)
      
      if next_date < self._farthest_date_relevant:
        continue
      
      financial_report = None
      try:
        financial_report = FinancialReport()
        financial_report.date = next_date
        financial_report.company_acronym = task.company_acronym
      except RuntimeError as err:
        err_msg = "%s -- gatherFinancialData -- Failed to initiate FinancialReport.\n%s" % (
          self._class_name,
          str(err)
        )
        raise RuntimeError(err_msg)
      
      html_with_10k_report = None
      try:
        task.progress = Progress.QUERYING_FOR_10K_REPORT_CONTENTS
        self._backend_tasks.updateTaskProgressBy(task)
        sleep(1)
        html_with_10k_report = self._sec_communicator.get10KReport(company_id, accession_number)

        if not html_with_10k_report:
          self._debug("getFinancialData", "\tExpected to get Html with 10K Report for %s, but got None" % date_str)
          continue
      except RuntimeError as err:
        err_msg = "%s -- gatherFinancialData -- Failed to obtain Html with 10K Report for %s.\n%s" % (
          self._class_name,
          date_str,
          str(err)
        )
        raise RuntimeError(err_msg)

      financial_statement_types = None
      try:
        task.progress = Progress.QUERYING_FOR_FINANCIAL_STMNT_TYPES
        self._backend_tasks.updateTaskProgressBy(task)
        sleep(1)
        financial_statement_types = self._sec_communicator.getFinancialStatementsTypes(html_with_10k_report)

        if not financial_statement_types:
          msg = "\tExpected to get Financial Statement Types for %s, but got None" % date_str
          self._debug("getFinancialData", msg)
          continue
      except RuntimeError as err:
        err_msg = "%s -- gatherFinancialData -- Failed to obtain Financial Statement Types for %s.\n%s" % (
          self._class_name,
          date_str,
          str(err)
        )
        raise RuntimeError(err_msg)

      for financial_statement_type in financial_statement_types:
        html_with_financial_statement = None
        try:
          task.progress = Progress.QUERYING_FOR_FINANCIAL_STMNT_CONTENTS
          self._backend_tasks.updateTaskProgressBy(task)
          html_with_financial_statement = self._sec_communicator.getFinancialStatement(
            company_id,
            accession_number,
            financial_statement_type
          )

          if not html_with_financial_statement:
            self._debug(
              "getFinancialData",
              "\tExpected to get HTML with Financial Statement for type %s, %s; but got None" % (
                financial_statement_type,
                date_str
              )
            )
            continue
        except RuntimeError as err:
          err_msg = "%s -- gatherFinancialData -- Failed to obtain HTML with Financial Statement for type %s, %s." % (
            self._class_name,
            financial_statement_type,
            date_str,
          )
          err_msg += "\n%s" % str(err)
          raise RuntimeError(err_msg)

        financial_data = None
        try:
          financial_data = self._sec_communicator.getDataFromFinancialStatement(html_with_financial_statement)
        
          if not financial_data or not financial_data[0]:
            self._debug(
              "getFinancialData",
              "\tExpected to get Financial Data for %s, %s, but got None" % (financial_statement_type, date_str)
            )
            continue
        except RuntimeError as err:
          err_msg = "%s -- gatherFinancialData" % self._class_name
          err_msg += " -- Failed to obtain Financial data from HTML with Financial Statement for type %s, %s.\n%s" % (
            financial_statement_type,
            date_str,
            str(err_msg)
          )
          raise RuntimeError(err_msg)
        
        if not financial_report.currencyUnitsUpdated() and financial_data[1]:
          try:
            financial_report.currency_units = financial_data[1]
          except RuntimeError as err:
            err_msg = "%s -- gatherFinancialData -- Failed to update the currency units for FinancialReport.\n%s" % (
              self._class_name,
              str(err)
            )
            raise RuntimeError(err_msg)
        
        existing_financial_measurements = financial_report.measurements
        financial_report.measurements = existing_financial_measurements | financial_data[0]
      
      try:
        self._persistFinancialReport(financial_report)
      except RuntimeError as err:
        err_msg = "%s -- gatherFinancialData -- Failed to persist FinancialReport.\n%s" % (
          self._class_name,
          str(err)
        )
    
    try:
      task.progress = Progress.FINISHED
      self._backend_tasks.updateTaskProgressBy(task)
    except RuntimeError as err:
      err_msg = "%s -- gatherFinancialData -- Failed to update the Task progress to finished.\n%s" % (
        self._class_name,
        str(err)
      )
    self._debug("getFinancialData", "Finish")

  def _persistFinancialReport(self, financial_report):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - financial_report -- FinancialReport.
    """
    try:
      self._debug("_persistFinancialReport", "Start\nfinancial_report:\t%s" % str(financial_report))
      self._database.createFinancialReportDocument(financial_report.toDocument())
      self._debug("_persistFinancialReport", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- _persistFinancialReport -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
