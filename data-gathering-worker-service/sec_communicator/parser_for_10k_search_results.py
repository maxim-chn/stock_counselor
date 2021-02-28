from html.parser import HTMLParser
from re import search

class ParserFor10kSearchResults(HTMLParser):
  def getResult(self):
    return self._result

  def handle_starttag(self, tag, attrs):
    if not self._series_div_flag:
      self._series_div_flag = self._divWithIdSeriesDivReached(tag, attrs)
      return

    if not self._results_table_flag:
      self._results_table_flag = self._resultsTableReached(tag, attrs)
      return

    if not self._tr_flag:
      self._tr_flag = tag == "tr"
      return

    if not self._link_flag:
      self._link_flag = self._linkWithIdInteractiveDataBtnReached(tag, attrs)
      if self._link_flag:
        href = attrs[0][1]
        acc_no = None
        match = search('accession_number=(.+?)&', href)
        if match:
          acc_no = match.group(1)
          acc_no = acc_no.translate({ord(c): None for c in '-'})
        self._retrieved_acc_no = acc_no
      return

  def handle_endtag(self, tag):
    if self._series_div_flag:
      if tag == "div":
        self._series_div_flag = False
        return

    if self._results_table_flag:
      if tag == "table":
        self._results_table_flag = False
        return

    if self._tr_flag:
      if tag == "tr":
        self._tr_flag = False

    if self._link_flag:
      if tag == "a":
        self._link_flag = False

  def handle_data(self, data):
    if not self._data_10k_flag:
      if self._series_div_flag and self._results_table_flag and self._tr_flag:
        if data == "10-K":
          self._data_10k_flag = True
          return

    if self._retrieved_acc_no:
      if "201" in data or "202" in data:
        self._result[data] = self._retrieved_acc_no
        self._retrieved_acc_no = None
        self._data_10k_flag = False
        return

  def initFlagsAndResult(self):
    self._result = dict()
    self._series_div_flag = False
    self._results_table_flag = False
    self._tr_flag = False
    self._data_10k_flag = False
    self._link_flag = False
    self._retrieved_acc_no = None

  def _divWithIdSeriesDivReached(self, tag, attrs):
    if not tag == "div" or not len(attrs) > 0:
      return False
    if not attrs[0][0] == 'id' or not attrs[0][1] == 'seriesDiv':
      return False
    return True

  def _linkWithIdInteractiveDataBtnReached(self, tag, attrs):
    if not tag == "a" or not len(attrs) > 1:
      return False
    if not attrs[1][0] == "id" or not attrs[1][1] == "interactiveDataBtn":
      return False
    return True

  def _resultsTableReached(self, tag, attrs):
    if not tag == "table" or not len(attrs) > 1:
      return False
    if not attrs[0][0] == 'class' or not attrs[0][1] == 'tableFile2':
      return False
    if not attrs[1][0] == 'summary' or not attrs[1][1] == 'Results':
      return False
    return True

