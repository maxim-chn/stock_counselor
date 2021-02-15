"""
Communicate with in-memory database of stock data miner tasks

"""
import json
import logging
from os import path

class BackendTasks:
  """
  database_connection - dictionary

  """
  def __init__(self, database_connection=dict()):
    # TODO: connect to module that communicates with RAM
    # TODO: implement singleton
    self._database_connection = database_connection


  def createTaskByCompanyAcronym(self, company_acronym, progress):
    msg = '%s - %s() - Start - company_acronym: %s, progress: %s' % (
      "BackendTasks",
      "createTaskByCompanyAcronym",
      company_acronym,
      progress
    )
    logging.getLogger('stock_data_miner').debug(msg)

    task = {"acronym": company_acronym, "progress": progress}
    relative_location = self._getRelativeLocation(company_acronym)
    with open(relative_location, "w") as write_file:
        json.dump(task, write_file)
    result = "task has been created"

    msg = '%s - %s() - Finish - result: %s' % (
      "BackendTasks",
      "createTaskByCompanyAcronym",
      result
    )
    logging.getLogger('stock_data_miner').debug(msg)

    return result


  def getTaskByCompanyAcronym(self, company_acronym):
    msg = '%s - %s() - Start - company_acronym: %s' % (
      "BackendTasks",
      "getTaskByCompanyAcronym",
      company_acronym
    )
    logging.getLogger('stock_data_miner').debug(msg)
    relative_location = self._getRelativeLocation(company_acronym)
    result = None
    if path.exists(relative_location):
      with open(relative_location, "r") as read_file:
        result = json.load(read_file)

    msg = '%s - %s() - Finish - result: %s' % (
      "BackendTasks",
      "getTaskByCompanyAcronym",
      result
    )
    logging.getLogger('stock_data_miner').debug(msg)

    return result

  def _getRelativeLocation(self, company_acronym):
    return "backend_tasks/remove_in_alpha/{}.json".format(company_acronym)