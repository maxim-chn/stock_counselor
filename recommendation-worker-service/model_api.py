from common_classes.loggable import Loggable
from os import path
from json import dumps, load

class ModelApi(Loggable):
  def __init__(self):
    super().__init__("ModelApi")


  def getUserProfileByUserId(self, user_id):
    file_path = path.join(
      path.dirname(__file__),
      "worker",
      '%s.json' % user_id
    )
    with open(file_path, "r") as read_file:
        result = load(read_file)
    return result

  def getCompaniesFinancialData(self):
    return iter(self)


  def __iter__(self):
    self._financial_document_ids = self._getAllFinancialDocumentIds()
    return self


  def __next__(self):
    financial_document_id = self._financial_document_ids.pop(0)
    file_path = path.join(
      path.dirname(__file__),
      "worker",
      financial_document_id
    )
    with open(file_path, "r") as read_file:
        result = load(read_file)
    return result


  def _getAllFinancialDocumentIds(self):
    return ["example_msft.json"]

