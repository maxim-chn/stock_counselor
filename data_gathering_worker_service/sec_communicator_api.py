from common_classes.loggable import Loggable
from json import dumps, load
from os import path
from requests import post, get
from sec_communicator.parser_for_10k_search_results import ParserFor10kSearchResults
from sec_communicator.parser_for_income_statements_ids import ParserForIncomeStatementsIds
from sec_communicator.parser_for_financial_statement import ParserForFinancialStatement

class SecCommunicatorApi(Loggable):
  """
  Reveals an internal API for retrieving financial data from the
  U.S. Securities And Exchange Commission website at https://www.sec.gov/
  """

  def __init__(self):
    super().__init__("SecCommunicatorApi")
    self._urls = self._loadHttpRequestsToSecConfigurations()
    self._parser_for_10k_search_results = ParserFor10kSearchResults()
    self._parser_for_income_statements_ids = ParserForIncomeStatementsIds()
    self._parser_for_financial_statement = ParserForFinancialStatement()

  def get10kAccessionNumbers(self, available_financial_reports):
    """
    Returns a dict where a key is a str with the 10-K financial report date and
    a value is it's unique id at the https://www.sec.gov/.

    Keyword arguments:
      available_financial_reports -- str -- HTML Document with the financial reports available for a company.
    """
    self._debug("get10kAccessionNumbers", "Start")
    result = None

    self._parser_for_10k_search_results.initFlagsAndResult()
    self._parser_for_10k_search_results.feed(available_financial_reports)
    result = self._parser_for_10k_search_results.getResult()

    self._debug("get10kAccessionNumbers", "Finish - result: %s" % result)
    return result

  def get10KReport(self, company_id, accession_number):
    """
    Returns a str with the HTML Document that contains 10-K financial report for a company.
    The report is expected to include the available financial statements types, i.e. Balance Sheets.
    None is returned in case the method faces an unexpected execution.

    Keyword arguments:
      company_id -- str -- unique company id at the https://www.sec.gov/
      accession_number -- str -- unique 10-K report id at the https://www.sec.gov/.
    """
    self._debug(
      "get10KReport",
      "Start - company_id: %s, accession_number: %s" % (company_id, accession_number)
    )
    result = None

    config = self._urls["obtain_income_statement_ids"]
    dst_url = config["url"]
    req_headers = config["headers"]
    req_params = config["params"]
    req_params["accession_number"] = accession_number
    req_params["cik"] = company_id

    try:
      res = get(dst_url, headers=req_headers, params=req_params)

      if not res.status_code == 200:
        err_msg = "actual response status code VS expected: %d VS %d" % (res.status_code, 200)
        raise RuntimeError(err_msg)

      if not res.headers["Content-Type"] == req_headers["Accept"]:
        err_msg = "actual response content-type VS expected: %s VS %s" % (
          res.headers["Content-Type"],
          req_headers["Accept"]
        )
        raise RuntimeError(err_msg)

      result = res.text

    except RuntimeError as err:
      self._error("get10KReport", "Error - %s" % err)

    finally:
      if result:
        self._debug("get10KReport", "Finish - result has %d characters" % len(result))
      else:
        self._debug("get10KReport", "Finish - result: None")

      return result

  def get10kReportsSearchResults(self, company_id):
    """
    Returns a str with the HTML Document that contains search results for the 10-K financial reports for a
    certain company, i.e. Microsoft, at the https://www.sec.gov/.
    None is returned if the method faces an unexpected execution.

    Keyword arguments:
      company_id -- str -- unique id of a company, i.e. Microsoft at the https://www.sec.gov/.
    """
    self._debug("get10kReportsSearchResults", "Start - company_id: %s" % company_id)
    result = None

    config = self._urls["obtain_10k_filings"]
    dst_url = config["url"]
    req_headers = config["headers"]
    req_params = config["params"]
    req_params["CIK"] = company_id

    try:
      res = get(dst_url, headers=req_headers, params=req_params)

      if not res.status_code == 200:
        err_msg = "actual response status code VS expected: %d VS %d" % (res.status_code, 200)
        raise RuntimeError(err_msg)

      if not res.headers["Content-Type"] == req_headers["Accept"]:
        err_msg = "actual response content-type VS expected: %s VS %s" % (
          res.headers["Content-Type"],
          req_headers["Accept"]
        )
        raise RuntimeError(err_msg)

      result = res.text

    except RuntimeError as err:
      self._error("get10kReportsSearchResults", "Error - %s" % err)

    finally:
      if result:
        self._debug("get10kReportsSearchResults", "Finish - result has %d characters" % len(result))
      else:
        self._debug("get10kReportsSearchResults", "Finish - result: None")

      return result

  def getCompanyId(self, acronym):
    """
    Returns a str that represents the unique id of a company, i.e. Microsoft, at the https://www.sec.gov/.
    None is returned in case the method faces an unexpected execution flow.

    Keyword arguments:
      acronym -- str -- the id at the stock exchange, i.e. NASDAQ, of a company.
    """
    self._debug("getCompanyId", "Start - acronym: %s" % acronym)
    result = None

    config = self._urls["obtain_company_id"]
    dst_url = config["url"]
    req_headers = config["headers"]
    req_payload = config["payload"]
    req_payload["keysTyped"] = acronym

    try:
      res = post(dst_url, data=dumps(req_payload), headers=req_headers)

      if not res.status_code == 200:
        err_msg = "actual response status code VS expected: %d VS %d" % (res.status_code, 200)
        raise RuntimeError(err_msg)

      if not res.headers["Content-Type"] == req_headers["Accept"]:
        err_msg = "actual response content-type VS expected: %s VS %s" % (
          res.headers["Content-Type"],
          req_headers["Accept"]
        )
        raise RuntimeError(err_msg)

      res_payload = res.json()
      actual_acronym = res_payload["hits"]["hits"][0]["_source"]["tickers"].lower()

      if not actual_acronym == acronym:
        err_msg = "actual response acronym VS expected: %s VS %s" % (
          actual_acronym,
          acronym
        )
        raise RuntimeError(err_msg)
      result = res_payload["hits"]["hits"][0]["_id"]

    except (IndexError, RuntimeError) as err:
      self._error("getCompanyId", "Error - %s" % err)

    finally:
      self._debug("getCompanyId", "Finish - result: %s" % result)

      return result

  def getDataFromFinancialStatement(self, financial_statement):
    """
    Returns a tuple.
      At index 0 there is a dict with the financial data where a key is a str with date
      and a value is a dict with the financial data.
      At index 1 there is a str with the currency units.

    Keyword arguments:
      financial_statement -- str -- HTML Document with financial data, i.e Balance Sheets.
    """
    self._debug("getDataFromFinancialStatement", "Start")
    self._parser_for_financial_statement.initFlagsAndResult()
    self._parser_for_financial_statement.feed(financial_statement)
    result = self._parser_for_financial_statement.getResult()

    self._debug(
      "getDataFromFinancialStatement",
      "Finish - result: %s financial values, %s currency format" % (len(result[0].keys()), result[1])
    )
    return result

  def getFinancialStatement(self, company_id, accession_number, income_statement_id):
    """
    Returns a str that contains HTML Document with the financial data statement, i.e Balance Sheets.
    In case the method faces an unexpected execution, None is returned.

    Keyword arguments:
       company_id -- str -- unique company id at the https://www.sec.gov/
       accession_number -- str -- unique 10-K report id at the https://www.sec.gov/
       income_statement_id -- str -- financial statemet type id, i.e. R2 for Balance Sheets (not consistent)
    """
    self._debug(
      "getFinancialStatement",
      "Start - company_id: %s, accession_number: %s, income_statement_id: %s" % (
        company_id, accession_number, income_statement_id
      )
    )
    result = None

    config = self._urls["obtain_income_statement_data"]
    dst_url = config["url"]
    req_headers = config["headers"]
    dst_url += "/"+company_id+"/"+accession_number+"/"+income_statement_id+".htm"

    try:
      res = get(dst_url, headers=req_headers)

      if not res.status_code == 200:
        err_msg = "actual response status code VS expected: %d VS %d" % (res.status_code, 200)
        raise RuntimeError(err_msg)

      if not res.headers["Content-Type"] == req_headers["Accept"]:
        err_msg = "actual response content-type VS expected: %s VS %s" % (
          res.headers["Content-Type"],
          req_headers["Accept"]
        )
        raise RuntimeError(err_msg)

      result = res.text

    except RuntimeError as err:
      self._error("getFinancialStatement", "Error - %s" % err)

    finally:
      if result:
        self._debug("getFinancialStatement", "Finish result has %d characters" % len(result))
      else:
        self._debug("getFinancialStatement", "Finish - result: None")

      return result

  def getFinancialStatementsIds(self, report_10k):
    """
    Returns a list of str where each str represents the available types of
    financial statements, i.e. Balance Sheets, for the 10K Report.

    Keyword arguments:
      report_10k -- str -- HTML Document with the 10-K financial report.
    """
    self._debug("getFinancialStatementsIds", "Start")
    result = None

    self._parser_for_income_statements_ids.initFlagsAndResult()
    self._parser_for_income_statements_ids.feed(report_10k)
    result = self._parser_for_income_statements_ids.getResults()

    self._debug("getFinancialStatementsIds", "Finish - result: %s" % result)
    return result

  def _getHttpRequestsToSecConfigFile(self):
    """
    Returns a str that is the location of the configuration file for the HTTP requests to the
    https://www.sec.gov/.
    """
    return path.join(
      path.dirname( __file__ ),
      "sec_communicator",
      'http_requests_to_sec.json'
    )

  def _loadHttpRequestsToSecConfigurations(self):
    """
    Returns a dict with the configurations for the HTTP Requests to the http://www.sec.gov/.
    """
    with open(self._getHttpRequestsToSecConfigFile(), "r") as read_file:
        result = load(read_file)
    return result
