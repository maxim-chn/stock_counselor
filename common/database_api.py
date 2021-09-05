from json import load
from os.path import dirname, exists, join
from pymongo import MongoClient # https://github.com/mongodb/mongo-python-driver
from bson import ObjectId
from traceback import format_exc

class DatabaseApi:
  """
  Reveals API for database, i.e. MongoDB
  """

  def __init__(self, service_name):
    """
    Raises RuntimeError.
    Keyword argumets:
      service_name -- str
    """
    self._class_name = "DatabaseApi"
    self._max_error_chars = 5000
    self._max_wait_for_connection = 2000
    self._config = self._getMongoDbConfiguration(service_name)

  def createTaskDocument(self, document):
    """
    Returns void.
    Raises RuntimeError
    Keyword arguments:
      document -- dict.
    """
    try:
      self._create(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["task"]["database_name"],
        self._config["documents"]["task"]["collection_name"],
        document
      )
    except RuntimeError as err:
      err_msg = "%s -- createTaskDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)
  
  def createTestDocument(self, document):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      document -- dict.
    """
    try:
      self._create(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["test"]["database_name"],
        self._config["documents"]["test"]["collection_name"],
        document
      )
    except RuntimeError as err:
      err_msg = "%s -- createTestDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def deleteTestDocumentBy(self, filter):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      filter -- dict -- identifies documents to be deleted.
    """
    try:
      self._deleteBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["test"]["database_name"],
        self._config["documents"]["test"]["collection_name"],
        filter
      )
    except RuntimeError as err:
      err_msg = "%s -- deleteTestDocument -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

  def readTaskDocumentBy(self, filter):
    """
    Returns dict or None.
    Raises RuntimeError.
    Keyword arguments:
      filter -- dict -- identifies documents to be read.
    """
    result = None

    try:
      result = self._findOneBy(
        self._config["connection"]["host"],
        self._config["connection"]["port"],
        self._config["user"]["username"],
        self._config["user"]["password"],
        self._config["documents"]["task"]["database_name"],
        self._config["documents"]["task"]["collection_name"],
        filter
      )
    except RuntimeError as err:
      err_msg = "%s -- readTaskDocumentBy -- Failed\n%s" % (self._class_name, str(err))
      raise RuntimeError(err_msg)

    return result

  def _authenticateAs(self, client, username, password):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      client -- MongoClient.
      username -- str.
      password -- str.
    """
    try:
      client["users"].authenticate(username, password)
    except Exception as err:
      err_msg = "%s -- _authenticateAs -- Failed\n%s" % (self._class_name, format_exc(self._max_error_chars, err))
      raise RuntimeError(err_msg)

  def _create(self, host, port, username, password, database_name, collection_name, document):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      host -- str.
      port -- int.
      username -- str.
      password -- str.
      database_name -- str -- database where the query is to be executed.
      collection_name -- str -- collection name inside the database.
      document -- dict.
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
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)
    finally:
      if client and isinstance(client, MongoClient):
        client.close()

  def _deleteBy(self, host, port, username, password, database_name, collection_name, filter):
    """
    Returns void.
    Raises RuntimeError.
    Keyword arguments:
      host -- str.
      port -- int.
      username -- str.
      password -- str.
      database_name -- str -- database where the query is to be executed.
      collection_name -- str -- collection name inside the database.
      filter -- dict -- identifies documents to be deleted.
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
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)
    finally:
      if client and isinstance(client, MongoClient):
        client.close()

  def _findOneBy(self, host, port, username, password, database_name, collection_name, filter):
    """
    Returns dict or None.
    Raises RuntimeError.
    Keyword arguments:
      host -- str.
      port -- int.
      username -- str.
      password -- str.
      database_name -- str -- database where the query is to be executed.
      collection_name -- str -- collection name inside the database.
      filter -- dict -- identifies documents to be deleted.
    """
    client = None
    result = None
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
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)
    finally:
      if client and isinstance(client, MongoClient):
        client.close()

  def _getClient(self, host, port):
    """
    Returns MongoClient.
    Raises RuntimeError.
    Keyword arguments:
      host -- str.
      port -- int.
    """
    try:
      result = MongoClient(
        host,
        port,
        socketTimeoutMS=self._max_wait_for_connection,
        connectTimeoutMS=self._max_wait_for_connection,
        serverSelectionTimeoutMS=self._max_wait_for_connection
      )
      return result
    except Exception as err:
      err_msg = "%s -- _getClient -- Failed to initialize database client\n%s" % (
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def _getMongoDbConfiguration(self, service_name):
    """
    Returns dict.
    It is a JSON with configurations to connect to MongoDB.
    Raises RuntimeError.
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
        self._class_name,
        format_exc(self._max_error_chars, err)
      )
      raise RuntimeError(err_msg)
    
    return result
  
  def _updateBy(self, host, port, username, password, database_name, collection_name, new_values, filter):
    # TODO: implement
    pass
