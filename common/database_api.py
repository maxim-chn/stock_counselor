from json import load
from os.path import dirname, exists, join
from pymongo import MongoClient # https://github.com/mongodb/mongo-python-driver
from bson import ObjectId
from traceback import format_exc

from common.loggable_api import Loggable

class DatabaseApi(Loggable):
  """
  Reveals API for database, i.e. MongoDB
  """
  max_err_chars = 5000
  max_wait_for_connection = 2000

  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Arguments:
      - service_name -- str
    """
    super().__init__(service_name, "DatabaseApi")
    self._config = self._getMongoDbConfiguration(service_name)

  def createFinancialReportDocument(self, document):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - document -- dict.
    """
    try:
      self._debug("createFinancialReportDocument", "Start\ndocument:\t%s" % str(document))
      self._create(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["financial_report"]["database_name"],
        self._config["documents"]["financial_report"]["collection_name"],
        document
      )
      self._debug("createFinancialReportDocument", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- createFinancialReportDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def createInvestmentRecommendationDocument(self, document):
    """
    Returns InvestmentRecommendation or None.
    Raises RuntimeError.
      - user_id -- str -- Unique id of an ApplicativeUser at the database.
    """
    try:
      self._debug("createInvestmentRecommendationDocument", "Start\ndocument:\t%s" % str(document))
      self._create(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["investment_recommendation"]["database_name"],
        self._config["documents"]["investment_recommendation"]["collection_name"],
        document
      )
      self._debug("createInvestmentRecommendationDocument", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- createInvestmentRecommendationDocument -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def createTaskDocument(self, document):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - document -- dict.
    """
    try:
      self._debug("createTaskDocument", "Started\ndocument:\t%s" % str(document))
      self._create(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["task"]["database_name"],
        self._config["documents"]["task"]["collection_name"],
        document
      )
      self._debug("createTaskDocument", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- createTaskDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def createTestDocument(self, document):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - document -- dict.
    """
    try:
      self._debug("createTestDocument", "Start\ndocument:\t%s" % str(document))
      self._create(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["test"]["database_name"],
        self._config["documents"]["test"]["collection_name"],
        document
      )
      self._debug("createTestDocument", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- createTestDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def deleteTaskDocumentBy(self, filter):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - filter -- dict -- identifies documents to be deleted.
    """
    try:
      self._debug("deleteTaskDocumentBy", "Start\nfilter:\t%s" % str(filter))
      self._deleteBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["task"]["database_name"],
        self._config["documents"]["task"]["collection_name"],
        filter
      )
      self._debug("deleteTaskDocumentBy", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- deleteTaskDocumentBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def deleteTestDocumentBy(self, filter):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - filter -- dict -- identifies documents to be deleted.
    """
    try:
      self._debug("deleteTestDocumentBy", "Start\nfilter:\t%s" % str(filter))
      self._deleteBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["test"]["database_name"],
        self._config["documents"]["test"]["collection_name"],
        filter
      )
      self._debug("deleteTestDocumentBy", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- deleteTestDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def getAcronymsForCompaniesWithFinancialReports(self):
    """
    Returns list<str>.
    Raises RuntimeError.
    """
    try:
      self._debug("getAcronymsForCompaniesWithFinancialReports", "Start")
      documents = self._findBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["financial_report"]["database_name"],
        self._config["documents"]["financial_report"]["collection_name"],
        { "company_acronym": { "$exists": True } }
      )
      
      result = []
      for document in documents:
        company_acronym = document["company_acronym"]
        if not company_acronym in result:
          result.append(company_acronym)
      
      self._debug("getAcronymsForCompaniesWithFinancialReports", "Finish\nresult:\t%s" % str(result))
      return result
    except RuntimeError as err:
      err_msg = "%s -- getAcronymsForCompaniesWithFinancialReports -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def readApplicativeUserDocumentBy(self, filter):
    """
    Returns dict or None.
    Raises RuntimeError.
    Arguments:
      - filter -- dict -- identifies documents to be read.
    """
    try:
      self._debug("readApplicativeUserDocumentBy", "Start\nfilter:\t%s" % str(filter))
      result = self._findOneBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["applicative_user"]["database_name"],
        self._config["documents"]["applicative_user"]["collection_name"],
        filter
      )
      self._debug("readApplicativeUserDocumentBy", "Finish\nresult:\t%s" % str(result))
      return result
    except RuntimeError as err:
      err_msg = "%s -- readApplicativeUserDocumentBy -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def readFinancialReportDocumentsBy(self, filter):
    """
    Returns list<dict> or None.
    Raises RuntimeError.
    Arguments:
      - filter -- dict -- identifies documents to be read.
    """
    try:
      self._debug("readFinancialReportDocumentsBy", "Start\nfilter:\t%s" % str(filter))
      result = self._findBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["financial_report"]["database_name"],
        self._config["documents"]["financial_report"]["collection_name"],
        filter
      )
      self._debug("readFinancialReportDocumentsBy", "Finish\nresult:\t%s" % str(result))
      return result
    except RuntimeError as err:
      err_msg = "%s -- readFinancialReportDocumentsBy -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def readFinancialUserProfileDocumentBy(self, filter):
    """
    Returns dict or None.
    Raises RuntimeError.
    Arguments:
      - filter -- dict -- identifies documents to be read.
    """
    try:
      self._debug("readFinancialUserProfileDocumentBy", "Start\nfilter:\t%s" % str(filter))
      result = self._findOneBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["financial_user_profile"]["database_name"],
        self._config["documents"]["financial_user_profile"]["collection_name"],
        filter
      )
      self._debug("readFinancialUserProfileDocumentBy", "Finish\nresult:\t%s" % str(result))
      return result
    except RuntimeError as err:
      err_msg = "%s -- readFinancialUserProfileDocumentBy -- Failed.\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def readTaskDocumentBy(self, filter):
    """
    Returns dict or None.
    Raises RuntimeError.
    Arguments:
      - filter -- dict -- identifies documents to be read.
    """
    try:
      self._debug("readTaskDocumentBy", "Start\nfilter:\t%s" % str(filter))
      result = self._findOneBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["task"]["database_name"],
        self._config["documents"]["task"]["collection_name"],
        filter
      )
      self._debug("readTaskDocumentBy", "Finish\nresult:\t%s" % str(result))
      return result
    except RuntimeError as err:
      err_msg = "%s -- readTaskDocumentBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def updateTaskDocument(self, new_values, filter_by):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - document -- dict.
    """
    try:
      self._debug("updateTaskDocument", "Start\nnew_values:\t%s\nfilter_by:\t%s" % (str(new_values), str(filter_by)))
      self._update(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["task"]["database_name"],
        self._config["documents"]["task"]["collection_name"],
        { "$set": new_values },
        filter_by
      )
      self._debug("updateTaskDocument", "Finish")
    except RuntimeError as err:
      err_msg = "%s -- updateTaskDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def _authenticateAs(self, client, username, password):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - client -- MongoClient.
      - username -- str.
      - password -- str.
    """
    try:
      client["non_applicative_users"].authenticate(username, password)
    except Exception as err:
      err_msg = "%s -- _authenticateAs -- Failed\n%s" % (
        self._class_name, format_exc(DatabaseApi.max_err_chars, err)
      )
      raise RuntimeError(err_msg)

  def _create(self, host, port, username, password, database_name, collection_name, document):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - host -- str.
      - port -- int.
      - username -- str.
      - password -- str.
      - database_name -- str -- database where the query is to be executed.
      - collection_name -- str -- collection name inside the database.
      - document -- dict.
    """
    client = None
    try:
      client = self._getClient(host, port)
      self._authenticateAs(client, username, password)
      database = client[database_name]
      collection = database[collection_name]
      object_id = collection.insert_one(document).inserted_id
      if object_id and isinstance(object_id, ObjectId):
        return
      raise RuntimeError("Document was not persisted as expected")
    except RuntimeError as err:
      err_msg = "%s -- _create -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- _create -- Failed during the insert query\n%s" % (
        self._class_name, format_exc(DatabaseApi.max_err_chars, err)
      )
      raise RuntimeError(err_msg)
    finally:
      if client and isinstance(client, MongoClient):
        client.close()

  def _deleteBy(self, host, port, username, password, database_name, collection_name, filter):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - host -- str.
      - port -- int.
      - username -- str.
      - password -- str.
      - database_name -- str -- database where the query is to be executed.
      - collection_name -- str -- collection name inside the database.
      - filter -- dict -- identifies documents to be deleted.
    """
    client = None
    try:
      client = self._getClient(host, port)
      self._authenticateAs(client, username, password)
      database = client[database_name]
      collection = database[collection_name]
      removed_document = collection.delete_one(filter)
      if removed_document.deleted_count > 0:
        return
      raise RuntimeError("No documents were found to delete")
    except RuntimeError as err:
      err_msg = "%s -- _deleteBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- _deleteBy -- Failed during the delete query\n%s" % (
        self._class_name, format_exc(DatabaseApi.max_err_chars, err)
      )
      raise RuntimeError(err_msg)
    finally:
      if client and isinstance(client, MongoClient):
        client.close()

  def _findBy(self, host, port, username, password, database_name, collection_name, filter):
    """
    Returns list<dict>.
    Raises RuntimeError.
    Arguments:
      - host -- str.
      - port -- int.
      - username -- str.
      - password -- str.
      - database_name -- str -- database where the query is to be executed.
      - collection_name -- str -- collection name inside the database.
      - filter -- dict -- identifies the desired documents.
    """
    client = None
    try:
      client = self._getClient(host, port)
      self._authenticateAs(client, username, password)
      database = client[database_name]
      collection = database[collection_name]
      cursor = collection.find(filter)
      
      result = []
      for document in cursor:
        result.append(document)
      
      client.close()
      return result
    except RuntimeError as err:
      err_msg = "%s -- _findBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- _findBy -- Failed during the find_one query\n%s" % (
        self._class_name, format_exc(DatabaseApi.max_err_chars, err)
      )
      raise RuntimeError(err_msg)
    finally:
      if client and isinstance(client, MongoClient):
        client.close()
  
  def _findOneBy(self, host, port, username, password, database_name, collection_name, filter):
    """
    Returns dict or None.
    Raises RuntimeError.
    Arguments:
      - host -- str.
      - port -- int.
      - username -- str.
      - password -- str.
      - database_name -- str -- database where the query is to be executed.
      - collection_name -- str -- collection name inside the database.
      - filter -- dict -- identifies the desired document.
    """
    client = None
    try:
      client = self._getClient(host, port)
      self._authenticateAs(client, username, password)
      database = client[database_name]
      collection = database[collection_name]
      result = collection.find_one(filter)
      client.close()
      return result
    except RuntimeError as err:
      err_msg = "%s -- _findOneBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- _findOneBy -- Failed during the find_one query\n%s" % (
        self._class_name, format_exc(DatabaseApi.max_err_chars, err)
      )
      raise RuntimeError(err_msg)
    finally:
      if client and isinstance(client, MongoClient):
        client.close()

  def _getClient(self, host, port):
    """
    Returns MongoClient.
    Raises RuntimeError.
    Arguments:
      - host -- str.
      - port -- int.
    """
    try:
      result = MongoClient(
        host,
        port,
        socketTimeoutMS=DatabaseApi.max_wait_for_connection,
        connectTimeoutMS=DatabaseApi.max_wait_for_connection,
        serverSelectionTimeoutMS=DatabaseApi.max_wait_for_connection
      )
      return result
    except Exception as err:
      err_msg = "%s -- _getClient -- Failed to initialize database client\n%s" % (
        self._class_name, format_exc(DatabaseApi.max_err_chars, err)
      )
      raise RuntimeError(err_msg)

  def _getMongoDbConfiguration(self, service_name):
    """
    Returns dict.
    It is a JSON with configurations to connect to MongoDB.
    Raises RuntimeError.
    Arguments:
      - service_name -- str.
    """
    result = dict()
    
    try:
      path_to_config = join(dirname(__file__), "database", "%s.json" % service_name)
      if exists(path_to_config):
        with open(path_to_config, "r") as read_file:
          result = load(read_file)
          read_file.close()
    except Exception as err:
      err_msg = "%s -- _getMongoDbConfiguration -- Failed to read from the configuration file\nfile_path:\t %s" % (
        self._class_name, format_exc(DatabaseApi.max_err_chars, err)
      )
      raise RuntimeError(err_msg)
    
    return result
  
  def _update(self, host, port, username, password, database_name, collection_name, new_values, filter):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - host -- str.
      - port -- int.
      - username -- str.
      - password -- str.
      - database_name -- str -- database where the query is to be executed.
      - collection_name -- str -- collection name inside the database.
      - new_values -- dict.
      - filter -- dict
    """
    client = None
    try:
      client = self._getClient(host, port)
      self._authenticateAs(client, username, password)
      database = client[database_name]
      collection = database[collection_name]
      collection.update_one(filter, new_values)
    except RuntimeError as err:
      err_msg = "%s -- _update -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- _update -- Failed during the update query\n%s" % (
        self._class_name, format_exc(DatabaseApi.max_err_chars, err)
      )
      raise RuntimeError(err_msg)
    finally:
      if client and isinstance(client, MongoClient):
        client.close()
