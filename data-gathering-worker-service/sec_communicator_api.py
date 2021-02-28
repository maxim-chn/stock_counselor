"""
Reveals an internal API for retrieving data from U.S. Securities And Exchange Commission
"""

from common_classes.loggable import Loggable
from json import dumps, load
from os import path
from requests import post, get
from sec_communicator.parser_for_10k_search_results import ParserFor10kSearchResults
from sec_communicator.parser_for_income_statements_ids import ParserForIncomeStatementsIds
from sec_communicator.parser_for_financial_statement import ParserForFinancialStatement

class SecCommunicatorApi(Loggable):
  """
  urls - JSON
  parser_for_10k_search_results - ParserFor10kSearchResults
  parser_for_income_statements_ids - ParserForIncomeStatementsIds
  parser_for_financial_statement - ParserForFinancialStatement
  """
  def __init__(self):
    super().__init__("SecCommunicatorApi")
    self._urls = self._loadUrls()
    self._parser_for_10k_search_results = ParserFor10kSearchResults()
    self._parser_for_income_statements_ids = ParserForIncomeStatementsIds()
    self._parser_for_financial_statement = ParserForFinancialStatement()

  def getFinancialStatementWithHtmlDocument(self, html_document_with_financial_statement):
    self._debug("getFinancialStatementWithHtmlDocument", "Start")
    result = ()

    self._parser_for_financial_statement.initFlagsAndResult()
    self._parser_for_financial_statement.feed(html_document_with_financial_statement)
    result = self._parser_for_financial_statement.getResult()

    self._debug(
      "getFinancialStatementWithHtmlDocument",
      "Finish - result: %s financial values, %s currency format" % (len(result[0].keys()), result[1])
    )
    return result

  def getFinancialStatementDocument(self, company_id, accession_number, income_statement_id):
    self._debug(
      "getFinancialStatementDocument",
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
      self._error("getFinancialStatementDocument", "Error - %s" % err)

    finally:
      if result:
        self._debug("getFinancialStatementDocument", "Finish result has %d characters" % len(result))
      else:
        self._debug("getFinancialStatementDocument", "Finish - result: None")

      return result


  def get10KReportWithCikAndAccNo(self, company_id, accession_number):
    self._debug(
      "get10KReportWithCikAndAccNo",
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
      self._error("get10KReportWithCikAndAccNo", "Error - %s" % err)

    finally:
      if result:
        self._debug("get10KReportWithCikAndAccNo", "Finish - result has %d characters" % len(result))
      else:
        self._debug("get10KReportWithCikAndAccNo", "Finish - result: None")

      return result


  def getIncomeStatementsIdsFromHtmlDocument(self, html_with_10k_report):
    self._debug("getIncomeStatementsIdsFromHtmlDocument", "Start")
    result = None

    self._parser_for_income_statements_ids.initFlagsAndResult()
    self._parser_for_income_statements_ids.feed(html_with_10k_report)
    result = self._parser_for_income_statements_ids.getResults()

    self._debug("getIncomeStatementsIdsFromHtmlDocument", "Finish - result: %s" % result)
    return result

  def get10kAccNoFromHtmlDocument(self, html_with_search_results):
    self._debug("get10kAccNoFromHtmlDocument", "Start")
    result = None

    self._parser_for_10k_search_results.initFlagsAndResult()
    self._parser_for_10k_search_results.feed(html_with_search_results)
    result = self._parser_for_10k_search_results.getResult()

    self._debug("get10kAccNoFromHtmlDocument", "Finish - result: %s" % result)
    return result

  def get10kSearchResultsWithCompanyId(self, company_id):
    self._debug("get10kSearchResultsWithCompanyId", "Start - company_id: %s" % company_id)
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
      self._error("get10kSearchResultsWithCompanyId", "Error - %s" % err)

    finally:
      if result:
        self._debug("get10kSearchResultsWithCompanyId", "Finish - result has %d characters" % len(result))
      else:
        self._debug("get10kSearchResultsWithCompanyId", "Finish - result: None")

      return result

  def getCompanyIdWithAcronym(self, acronym):
    self._debug("getCompanyIdWithAcronym", "Start - acronym: %s" % acronym)
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
      self._error("getCompanyIdWithAcronym", "Error - %s" % err)

    finally:
      self._debug("getCompanyIdWithAcronym", "Finish - result: %s" % result)

      return result

  def _getRelativeLocationOfUrlsFile(self):
    return path.join(
      path.dirname( __file__ ),
      "sec_communicator",
      'urls.json'
    )

  def _loadUrls(self):
    result = None
    with open(self._getRelativeLocationOfUrlsFile(), "r") as read_file:
        result = load(read_file)
    return result
