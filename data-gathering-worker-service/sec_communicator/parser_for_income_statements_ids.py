from html.parser import HTMLParser

class ParserForIncomeStatementsIds(HTMLParser):
  def getResults(self):
    return self._results

  def handle_starttag(self, tag, attrs):
    if not self._link_flag and not self._financial_statements_flag:
      self._link_flag = tag == 'a'
      return

    if not self._ul_flag:
      self._ul_flag = tag == 'ul'
      return

    if tag == 'li' and len(attrs) > 1:
      self._results.append(attrs[1][1].upper())

  def handle_endtag(self, tag):
    if self._link_flag:
      if tag == "a":
        self._link_flag = False
        return

    if self._ul_flag:
      if tag == "ul":
        self._ul_flag = False
        self._financial_statements_flag = False
        return

  def handle_data(self, data):
    if not self._financial_statements_flag:
      if self._link_flag and data == 'Financial Statements':
        self._financial_statements_flag = True

  def initFlagsAndResult(self):
    self._results = []
    self._link_flag = False
    self._financial_statements_flag = False
    self._ul_flag = False

