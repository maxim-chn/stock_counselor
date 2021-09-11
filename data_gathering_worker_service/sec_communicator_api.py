from common.loggable_api import Loggable
from data_gathering_worker_service.sec_communicator.parser_for_10k_search_results import ParserFor10kSearchResults
from data_gathering_worker_service.sec_communicator.parser_for_income_statements_ids import FinancialStatementsIdsParser
from data_gathering_worker_service.sec_communicator.parser_for_financial_statement import FinancialStatementParser
from json import dumps, load
from os import path
from requests import post, get
from traceback import format_exc

class SecCommunicator(Loggable):
  """
  Reveals an internal API for retrieving financial data from the U.S. Securities And Exchange Commission
  official website at https://www.sec.gov/
  """

  def __init__(self, service_name):
    """
    Keyword arguments:
      service_name -- str.
    """
    super().__init__(service_name, "SecCommunicator")
    self._max_error_chars = 5000
    self._reqs_to_sec_config = self._loadHttpRequestsToSecConfigurations()
    self._parser_for_10k_search_results = ParserFor10kSearchResults()
    self._financial_statements_ids_parser = FinancialStatementsIdsParser()
    self._financial_statement_parser = FinancialStatementParser()

  def get10kAccessionNumbers(self, available_financial_reports):
    """
    Returns dict.
     - key -- str -- represents 10-K financial report date.
     - value -- str -- unique 10-K financial report id at the EDGAR database.
    Raises RuntimeError.
    Keyword arguments:
      available_financial_reports -- str -- HTML Document with the financial statements available for a company.
    """
    try:
      self._debug("get10kAccessionNumbers", "Start")
      
      self._parser_for_10k_search_results.initFlagsAndResult()
      self._parser_for_10k_search_results.feed(available_financial_reports)
      result = self._parser_for_10k_search_results.getResult()
      
      self._debug("get10kAccessionNumbers", "Finish\nresult:\t%s" % result)
      return result
    except Exception as err:
      err_msg = "%s -- get10kAccessionNumbers -- Failed\n%s" % (
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def get10KReport(self, company_id, accession_number):
    """
    Returns str or None.
    Raises RuntimeError.
    Retrieves a HTML Document with the 10-K financial report.
    The report is expected to include the available financial statements types, i.e. Balance Sheets.
    Keyword arguments:
      accession_number -- str -- unique 10-K report id at the EDGAR database.
      company_id -- str -- unique company id at the EDGAR database.
    """
    try:
      self._debug("get10KReport", "Start\ncompany_id:\t%s\naccession_number:\t%s" % (company_id, accession_number))
      
      result = None
      config = self._reqs_to_sec_config["obtain_income_statement_ids"]
      dst_url = config["url"]
      req_headers = config["headers"]
      req_params = config["params"]
      req_params["accession_number"] = accession_number
      req_params["cik"] = company_id
      
      sec_response = get(dst_url, headers=req_headers, params=req_params)
      self._isSecReponseStatusCodeValid(sec_response, 200)
      self._isSecResponseContentTypeValid(sec_response, req_headers["Accept"])
      result = sec_response.text
      
      if result:
        self._debug("get10KReport", "Finish\nresult has %d characters" % len(result))
      else:
        self._debug("get10KReport", "Finish\nresult: None")
      return result
    except RuntimeError as err:
      err_msg = "%s -- get10KReport -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- get10KReport -- Failed\n%s" % (
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def get10kReportsSearchResults(self, company_id):
    """
    Returns str or None.
    Raises RuntimeError.
    Retrieves HTML Document with the search results for the 10-K financial reports.
    Keyword arguments:
      company_id -- str -- unique company id at the EDGAR database.
    """
    try:
      self._debug("get10kReportsSearchResults", "Start\ncompany_id:\t%s" % company_id)
      result = None
      config = self._reqs_to_sec_config["obtain_10k_filings"]
      dst_url = config["url"]
      req_headers = config["headers"]
      req_params = config["params"]
      req_params["CIK"] = company_id
      
      sec_response = get(dst_url, headers=req_headers, params=req_params)
      self._isSecReponseStatusCodeValid(sec_response, 200)
      self._isSecResponseContentTypeValid(sec_response, req_headers["Accept"])
      result = sec_response.text
      
      if result:
        self._debug("get10kReportsSearchResults", "Finish\nresult has %d characters" % len(result))
      else:
        self._debug("get10kReportsSearchResults", "Finish\nresult: None")
      return result
    except RuntimeError as err:
      err_msg = "%s -- get10kReportsSearchResults -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- get10kReportsSearchResults -- Failed\n%s" % (
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def getCompanyId(self, company_acronym):
    """
    Returns str or None.
    Retrieves the unique id of a company, i.e. Microsoft, at the EDGAR database.
    Keyword arguments:
      company_acronym -- str -- the company symbol at a stock exchange, i.e. NASDAQ.
    """
    try:
      self._debug("getCompanyId", "Start\nacronym:\t%s" % company_acronym)
      
      result = None
      config = self._reqs_to_sec_config["obtain_company_id"]
      dst_url = config["url"]
      req_headers = config["headers"]
      req_payload = config["payload"]
      req_payload["keysTyped"] = company_acronym
      
      sec_response = post(dst_url, data=dumps(req_payload), headers=req_headers)
      self._isSecReponseStatusCodeValid(sec_response, 200)
      self._isSecResponseContentTypeValid(sec_response, req_headers["Accept"])
      response_data = sec_response.json()
      self._isCompanyAcronymInSecResponseValid(response_data, company_acronym)
      result = response_data["hits"]["hits"][0]["_id"]
      self._debug("getCompanyId", "Finish\nresult:\t%s" % result)
      return result
    except RuntimeError as err:
      err_msg = "%s -- getCompanyId -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- getCompanyId -- Failed\n%s" % (self._class_name, format_exc(self._max_error_chars, err))
      raise RuntimeError(err_msg)

  def getDataFromFinancialStatement(self, financial_statement):
    """
    Returns a tuple.
      - index 0 -- dict -- includes the retrieved financial data from https://www.sec.gov/.
      - index 1 -- str -- currency units.
    Raises RuntimeError.
    Keyword arguments:
      financial_statement -- str -- HTML Document with the financial data.
    """
    try:
      self._debug("getDataFromFinancialStatement", "Start")
      
      self._financial_statement_parser.initFlagsAndResult()
      self._financial_statement_parser.feed(financial_statement)
      result = self._financial_statement_parser.getResult()
      
      self._debug(
        "getDataFromFinancialStatement",
        "Finish - result: %s financial values, %s currency units" % (len(result[0].keys()), result[1])
      )
      return result
    except Exception as err:
      err_msg = "%s -- getDataFromFinancialStatement -- Failed\n%s" % (
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def getFinancialStatement(self, company_id, accession_number, financial_statement_type):
    """
    Returns str or None.
    Raises RuntimeError.
    The str is a HTML Document with the financial data statement, i.e Balance Sheets.
    Keyword arguments:
      - accession_number -- str -- unique 10-K report id at the https://www.sec.gov/
      - company_id -- str -- unique company id at the https://www.sec.gov/
      - financial_statement_type -- str -- financial statement type id, i.e. R2.
    """
    try:
      self._debug(
        "getFinancialStatement",
        "Start - company_id: %s, accession_number: %s, income_statement_id: %s" % (
          company_id,
          accession_number,
          financial_statement_type
        )
      )
      
      result = None
      config = self._reqs_to_sec_config["obtain_income_statement_data"]
      dst_url = "%s/%s/%s/%s.htm" % (config["url"], company_id, accession_number, financial_statement_type)
      req_headers = config["headers"]
      
      sec_response = get(dst_url, headers=req_headers)
      self._isSecReponseStatusCodeValid(sec_response, 200)
      self._isSecResponseContentTypeValid(sec_response, req_headers["Accept"])
      result = sec_response.text
      
      if result:
        self._debug("getFinancialStatement", "Finish\nresult has %d characters" % len(result))
      else:
        self._debug("getFinancialStatement", "Finish\nresult: None")
      return result
    except RuntimeError as err:
      err_msg = "%s -- getFinancialStatement -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- getFinancialStatement -- Failed\n%s" % (
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def getFinancialStatementsTypes(self, report_10k):
    """
    Returns list.
    Raises RuntimeError.
    Each element is a str. It represents the available type of financial statements.
    Keyword arguments:
      report_10k -- str -- a HTML Document with the 10-K financial report.
    """
    try:
      self._debug("getFinancialStatementsTypes", "Start")
      
      self._financial_statements_ids_parser.initFlagsAndResult()
      self._financial_statements_ids_parser.feed(report_10k)
      result = self._financial_statements_ids_parser.getResults()
      
      self._debug("getFinancialStatementsTypes", "Finish\nresult:\t%s" % result)
      return result
    except Exception as err:
      err_msg = "%s -- getFinancialStatementsTypes -- Failed\n%s" % (
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)
    

  def _getHttpRequestsToSecConfigFile(self):
    """
    Returns path.
    It leads to the configuration file for the HTTP requests to the https://www.sec.gov/
    """
    return path.join(
      path.dirname( __file__ ),
      "sec_communicator",
      "http_requests_to_sec.json"
    )

  def _isCompanyAcronymInSecResponseValid(self, response_data, expected_val):
    """
    Raises a RuntimeError in case the company acrpnym in the response is not as expected.
    Keyword arguments:
      expected_val -- str -- company acronym.
      response_data -- dict -- a JSON format of the response from SEC.
    """
    actual_acronym = response_data["hits"]["hits"][0]["_source"]["tickers"].lower()
    if not actual_acronym == expected_val:
      raise RuntimeError(
        "Actual Company Acronym in SEC Response VS Expected: %s VS %s" % (actual_acronym, expected_val)
      )

  def _isSecResponseContentTypeValid(self, response, expected_val):
    """
    Raises a RuntimeError in case the response content-type header value is different
    from the request's accept header.
    Keyword arguments:
      expected_val -- str -- request's accept header value.
      response -- LocalResponse -- a HTTP response object that belongs to the Bottle framework.
    """
    if not response.headers["Content-Type"] == expected_val:
      raise RuntimeError("Response Content-Type VS Request Accept header: %s VS %s" % (
        response.headers["Content-Type"], expected_val
      ))

  def _isSecReponseStatusCodeValid(self, response, expected_val):
    """
    Raises a RuntimeError in case the actual status code is different from the expected.
    Keyword arguments:
      expected_val -- int -- represents a HTTP response status code.
      response -- LocalResponse -- a HTTP response object that belongs to the Bottle framework.
    """
    if not response.status_code == expected_val:
      raise RuntimeError(
        "Actual Response Status Code VS Expected: %d VS %d" % (response.status_code, expected_val)
      )

  def _loadHttpRequestsToSecConfigurations(self):
    """
    Returns a dict.
    It is the configurations for the HTTP Requests to the http://www.sec.gov/.
    """
    with open(self._getHttpRequestsToSecConfigFile(), "r") as read_file:
        result = load(read_file)
    return result
