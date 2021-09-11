from logging import getLogger
from common.data_gathering_backend_tasks_api import BackendTasks
from common.data_gathering.backend_tasks.task import Progress, Task
from common.database_api import DatabaseApi
from common.loggable_api import Loggable
from datetime import datetime
from data_gathering_worker_service.financial_report import FinancialReport
from data_gathering_worker_service.sec_communicator_api import SecCommunicator
from time import sleep
from traceback import format_exc

def startDataGatheringWorkerService(service_name):
  """
  Returns void.
  Raises RuntimeError.
  Subscribes to financial data gathering tasks with logic to execute them.
  Keyword arguments:
    service_name -- str.
  """
  def consumeFinancialDataGatheringMessages(ch, method, properties, body):
    """
    Returns void.
    Logic for the execution of the financial data gathering task.
    Keyword arguments:
      - ch -- Channel -- RabbitMq channel.
      - method -- ??? -- ???
      - properties -- ??? -- ???
      - body -- ??? -- contains the message.
    """
    service_name = "data_gathering_worker_service"
    worker = Worker(service_name)
    max_error_chars = 5000
    task = None
    
    try:
      published_message = body.decode("utf-8")
      task = Task.fromJson(published_message)
    except Exception as err:
      err_msg = "%s -- consumeFinancialDataGatheringMessages -- Failed to parse the published message to Task.\n%s" % (
        service_name,
        format_exc(max_error_chars, err)
      )
      getLogger(service_name).error(err_msg)
      return
    finally:
      ch.stop_consuming()

    try:
      worker.gatherFinancialData(task)
    except RuntimeError as err:
      err_msg = "%s -- consumeFinancialDataGatheringMessages -- Failed to execute the Task.\n%s" % (
        service_name,
        str(err)
      )
      getLogger(service_name).error(err_msg)
  
  try:
    backend_tasks = BackendTasks(service_name)
  except RuntimeError as err:
    err_msg = "%s -- startDataGatheringWorkerService -- Failed to initiate backend tasks object\n%s" % (
      service_name,
      str(err)
    )
    raise RuntimeError(err_msg)
  
  try:
    backend_tasks.consumeMessage(consumeFinancialDataGatheringMessages)
  except RuntimeError as err:
    err_msg = "%s -- startDataGatheringWorkerService -- Failed to subscribe to backend tasks\n%s" % (
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
    Keyword arguments:
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
    try:
      self._debug("getFinancialData", "Start\ntask:\t%s" % str(task))
      financial_reports = []
      
      task.progress = Progress.QUERYING_FOR_COMPANY_ID
      self._backend_tasks.updateTaskProgressBy(task)
      company_id = self._sec_communicator.getCompanyId(task.company_acronym)
      
      if not company_id:
        self._debug("getFinancialData", "Finish\nExpected to get Company Id, but got None")
        return
      
      task.progress = Progress.QUERYING_FOR_AVAILABLE_10K_REPORTS
      self._backend_tasks.updateTaskProgressBy(task)
      sleep(1)
      html_with_10k_search_results = self._sec_communicator.get10kReportsSearchResults(company_id)

      if not html_with_10k_search_results:
        self._debug("getFinancialData", "Finish\nExpected to get Html with 10K Search Results, but got None")
        return

      task.progress = Progress.QUERYING_FOR_10K_IDS
      self._backend_tasks.updateTaskProgressBy(task)
      sleep(1)
      accession_numbers = self._sec_communicator.get10kAccessionNumbers(html_with_10k_search_results)

      if not accession_numbers:
        self._debug(
          "getFinancialData",
          "Finish\nExpected to get mapping of years to accession numbers, but got empty dict"
        )
        return
      
      for date_str, accession_number in accession_numbers.items():
        next_date = datetime.strptime(date_str, self._date_format)
        
        if next_date < self._farthest_date_relevant:
          continue
        
        financial_report = FinancialReport()
        financial_report.date = next_date
        
        task.progress = Progress.QUERYING_FOR_10K_REPORT_CONTENTS
        self._backend_tasks.updateTaskProgressBy(task)
        sleep(1)
        html_with_10k_report = self._sec_communicator.get10KReport(company_id, accession_number)

        if not html_with_10k_report:
          self._debug("getFinancialData", "\tExpected to get Html with 10K Report for %s, but got None" % date_str)
          continue

        task.progress = Progress.QUERYING_FOR_FINANCIAL_STMNT_TYPES
        self._backend_tasks.updateTaskProgressBy(task)
        sleep(1)
        financial_statement_types = self._sec_communicator.getFinancialStatementsTypes(html_with_10k_report)

        if not financial_statement_types:
          self._debug("getFinancialData", "\tExpected to get Financial Statement Types for %s, but got None" % date_str)
          return

        for financial_statement_type in financial_statement_types:
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
              "\tExpected to get Financial Statement for type %s, %s, but got None" % (
                financial_statement_type,
                date_str
              )
            )
            continue

          financial_data = self._sec_communicator.getDataFromFinancialStatement(html_with_financial_statement)
          
          if not financial_data[0]:
            self._debug(
              "getFinancialData",
              "\tExpected to get Financial Data for %s, %s, but got None" % (financial_statement_type, date_str)
            )
            continue
          
          if not financial_report.currencyUnitsUpdated() and financial_data[1]:
            financial_report.currency_units = financial_data[1]
          
          existing_financial_measurements = financial_report.measurements
          financial_report.measurements = existing_financial_measurements | financial_data[0]
        
        financial_reports.append(financial_report)
      
      self._persistFinancialReports(financial_reports)
      
      task.progress = Progress.FINISHED
      self._backend_tasks.updateTaskProgressBy(task)
      
      self._debug("getFinancialData", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def _persistFinancialReport(self, financial_report):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      - financial_report -- FinancialReport.
    """
    try:
      self._debug("_persistFinancialReport", "Start\nfinancial_report:\t%s" % str(financial_report))
      self._database.createFinancialReportDocument(financial_report.toDocument())
      self._debug("_persistFinancialReport", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- _persistFinancialReport -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)


  def _persistFinancialReports(self, financial_reports):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      - financial_reports -- list -- contains FinancialReport objects.
    """
    try:
      self._debug("_persistFinancialReports", "Start\nAmount of years with financial report: %d" % len(financial_reports))
      for financial_report in financial_reports:
        self._persistFinancialReport(financial_report)
      self._debug("_persistFinancialReports", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- _persistFinancialReports -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    
