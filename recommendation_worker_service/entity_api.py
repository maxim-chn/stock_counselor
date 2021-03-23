from common.loggable_api import Loggable
from json import dump, load
from os import path, listdir

class Entity(Loggable):
  """
  This is our Entity Logic.
  It accesses the database records.
  TODO: remove in v1.0 the use of file system and integrate a database, i.e. MongoDb.
  """

  def __init__(self, log_id):
    """
    Keyword arguments:
      log_id -- str.
    """
    super().__init__(log_id, "Entity")
    self._financial_data_storage_files = []

  def getUserProfileByUserId(self, user_id):
    """
    Returns a dict.
    It contains the financial indicators that represent the user's investment preferences.
    Keyword arguments:
      user_id -- str -- an unique identifier of a user inside our program.
    """
    result = dict()
    user_profile_storage_path = self._getUserProfileStoragePath(user_id)
    if path.exists(user_profile_storage_path):
      with open(user_profile_storage_path, "r") as read_file:
        result = load(read_file)
    return result

  def getCompaniesFinancialData(self):
    """
    Returns an iter.
    The iterator allows to go over the financial data of the companies.
    """
    return iter(self)

  def storeRecommendation(self, recommendation):
    """
    TODO: replace in v1.0 to store in the actual database.
    Persists the investment recommendation.
    Keyword arguments:
      recommendation -- dict -- the investment recommendation for a user.
    """
    recommendation_storage_path = self._getRecommendationStoragePath(recommendation["user_id"])
    with open(recommendation_storage_path, "w+") as write_file:
      dump(recommendation, write_file)

  def _getFinancialDataStoragePaths(self):
    """
    TODO: Remove in v1.0
    Returns a list.
    It contains the absolute paths to the financial data storage files.
    """
    result = []
    financial_data_storage_dir_path = self._getFinancialDataStorageDir()
    for filename in listdir(financial_data_storage_dir_path):
      if filename.endswith("json"):
        result.append(path.join(financial_data_storage_dir_path, filename))
    return result

  def _getFinancialDataStorageDir(self):
    """
    TODO: remove in v1.0
    Returns a path
    It is the location of the the directory with the financial data storage files.
    """
    return path.join(
      path.dirname( __file__ ),
      "..",
      "common",
      "financial_data_db"
    )

  def _getRecommendationStoragePath(self, user_id):
    """
    TODO: remove in v1.0
    Returns a path.
    It is the location of the storage file for the investment recommendation
    Keyword arguments:
      user_id -- str -- an unique identifier of a user inside our program.
    """
    return path.join(
      path.dirname(__file__),
      "..",
      "common",
      "recommendations_db",
      "%s.json" % user_id
    )

  def _getUserProfileStoragePath(self, user_id):
    """
    TODO: remove in v1.0
    Returns a path.
    It is the location of the storage file with the user profile.
    Keyword arguments:
      user_id -- str -- an unique identifier of a user inside our program.
    """
    return path.join(
      path.dirname(__file__),
      "..",
      "common",
      "user_profiles_db",
      "%s.json" % user_id
    )

  def __iter__(self):
    """
    TODO: remove in v1.0 and adopt the iteration over the relevant database records.
    Initiates the list with the paths to the persisted financial data.
    """
    self._financial_data_storage_files = self._getFinancialDataStoragePaths()
    return self

  def __next__(self):
    """
    Returns a dict or raises the StopIteration error.
    The dict contains the financial data about a company.
    """
    if len(self._financial_data_storage_files) == 0:
      raise StopIteration()
    financial_storage_file_path = self._financial_data_storage_files.pop(0)
    with open(financial_storage_file_path, "r") as read_file:
      result = load(read_file)
    return result