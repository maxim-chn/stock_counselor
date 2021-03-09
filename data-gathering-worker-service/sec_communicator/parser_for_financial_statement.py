from re import sub

from html.parser import HTMLParser

class ParserForFinancialStatement(HTMLParser):
  def getResult(self):
    result = (self._financial_values, self._currency_units)
    return result

  def handle_starttag(self, tag, attrs):
    if not self._table_tag_flag:
      if tag == "table" and len(attrs) > 0 and attrs[0][1] == "report":
        self._table_tag_flag = True
        return

    if not self._strong_tag_flag:
      self._strong_tag_flag = tag == "strong"

    if not self._td_tag_flag:
      if tag == "td" and len(attrs) > 0:
        self._td_tag_flag = True
        if attrs[0][1] == "pl " or attrs[0][1] == "pl custom":
          self._class_pl_flag = True
          self._retrived_data_from_nump = False
          self._temp_key = None
          self._temp_value = None
        elif attrs[0][1] == "nump" or attrs[0][1] == "num":
          self._class_nump_flag = True
        elif attrs[0][1] == "text":
          if self._temp_key:
            self._temp_prefix_key = self._temp_key.replace(self._temp_prefix_key, "")
            self._temp_key = None
        return

    if not self._a_tag_flag:
      self._a_tag_flag = tag =="a"
      return

  def handle_endtag(self, tag):
    if self._table_tag_flag:
      if tag == "table":
        self._table_tag_flag = False
        return

    if self._strong_tag_flag:
      if tag == "strong":
        self._strong_tag_flag = False
        return

    if self._td_tag_flag:
      if tag == "td":
        self._td_tag_flag = False
        if self._class_pl_flag:
          self._class_pl_flag = False
        elif self._class_nump_flag:
          self._class_nump_flag = False
        return

    if self._a_tag_flag:
      if tag == "a":
        self._a_tag_flag = False
        return

  def handle_data(self, data):
    if self._table_tag_flag and self._strong_tag_flag:
      if "$ in" in data:
        self._currency_units = data.split("$ in ")[1]
      elif "$) in" in data:
        self._currency_units = data.split("$) in ")[1]
      return

    if self._td_tag_flag and self._class_pl_flag and self._a_tag_flag:
      data = sub("\n", "", data)
      data = sub("\t\t", "", data)
      data = sub("\t", " ", data)
      self._temp_key = "%s %s" % (self._temp_prefix_key, data)
      return

    if self._td_tag_flag and self._class_nump_flag and not self._retrived_data_from_nump:
      self._temp_value = sub("[\$ ,\,]", "", data)
      self._retrived_data_from_nump = True
      if not self._temp_key == None:
        self._financial_values[self._temp_key] = self._temp_value
      return

  def initFlagsAndResult(self):
    self._financial_values = dict()
    self._currency_units = None
    self._table_tag_flag = False
    self._strong_tag_flag = False
    self._class_pl_flag = False
    self._retrived_data_from_nump = False
    self._class_nump_flag = False
    self._a_tag_flag = False
    self._td_tag_flag = False
    self._temp_key = None
    self._temp_prefix_key = ""
    self._temp_value = None