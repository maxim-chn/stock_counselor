from pymongo import MongoClient, errors
from os import path
from json import load

def initializeMongoDb():
    config = loadConfiguration()
    initContainer(
        config["connection"]["port"],
        config["users"]["root"]["username"],
        config["users"]["root"]["password"],
        config["container"]["name"]
    )
    initAdmin(
        config["users"]["root"]["username"],
        config["users"]["root"]["password"],
        config["users"]["admin"]["username"],
        config["users"]["admin"]["password"]
    )
    client = initClient(
      config["connection"]["host"],
      config["connection"]["port"]
    )
    authenticateAsAnAdminUser(
      client,
      config["users"]["admin"]["username"],
      config["users"]["admin"]["password"]
    )
    dropFinancialDataDb(client)
    dropFinancialUserProfilesDb(client)
    dropRecommendationsDb(client)
    dropAllUsersFromUsersDb(client)
    dropUsersDb(client)
    createDataGatherer(client)
    createRecommender(client)
    client.close()

def authenticateAsAnAdminUser(client, username, password):
  print("[x] Authenticating as an admin")
  client["admin"].authenticate(username, password)
  print("\tAuthentication succeeded")

def createDataGatherer(client):
  print("[x] Creating data gatherer user")
  client["users"].command(
    "createUser",
    "data_gatherer",
    pwd="data_gatherer",
    roles=[
        {"role": "read", "db": "financial_data"},
        {"role": "readWrite", "db": "recommendations"},
        {"role": "read", "db": "financial_user_profiles"}
    ]
  )
  print("\tCreation of data gatherer succeeded")

def createRecommender(client):
  print("[x] Creating recommender user")
  client["users"].command(
    "createUser",
    "recommender",
    pwd="recommender",
    roles=[
      {"role": "read", "db": "financial_data"},
      {"role": "readWrite", "db": "recommendations"},
      {"role": "read", "db": "financial_user_profiles"}
    ]
  )
  print("\tCreation of recommender succeeded")

def dropAllUsersFromUsersDb(client):
  print("[x] Dropping all users associated with the users database")
  try:
    client["users"].command("dropUser", "data_gatherer")
  except errors.OperationFailure as e:
    if not "UserNotFound" in str(e):
      raise e
  try:
    client["users"].command("dropUser", "recommender")
  except errors.OperationFailure as e:
    if not "UserNotFound" in str(e):
      raise e
  print("\tDrop succeeded")

def dropFinancialDataDb(client):
  print("[x] Dropping financial_data database (if exists)")
  client["financial_data"].command("dropDatabase")
  print("\tDrop succeeded")

def dropFinancialUserProfilesDb(client):
  print("[x] Dropping financial_user_profiles database (if exists)")
  client["financial_user_profiles"].command("dropDatabase")
  print("\tDrop succeeded")

def dropRecommendationsDb(client):
  print("[x] Dropping recommendations database (if exists)")
  client["recommendations"].command("dropDatabase")
  print("\tDrop succeeded")

def dropUsersDb(client):
  print("[x] Dropping users database (if exists)")
  client["users"].command("dropDatabase")
  print("\tDrop succeeded")

def initAdmin(root_username, root_password, admin_username, admin_password):
  print("[x] Connect to MongoDb CLI\n$ mongo")
  input()
  print("[x] Switch to admin database\n$ use admin")
  input()
  print("[x] Authenticate as a root user\n$ db.auth(\"%s\", \"%s\")" % (root_username, root_password))
  input()
  command = "db.createUser({ user: \"%s\", pwd: \"%s\"," % (admin_username, admin_password)
  command = command + "roles: [\n"
  command = command + "{ role: \"dbOwner\", db: \"users\"}\n"
  command = command + ", { role: \"dbOwner\", db: \"financial_data\"}\n"
  command = command + ", { role: \"dbOwner\", db: \"recommendations\"}\n"
  command = command + ", { role: \"dbOwner\", db: \"financial_user_profiles\"}\n"
  command = command + "] })"
  print("[x] Create admin user\n$ %s" % command)
  input()

def initClient(host, port):
  print("[x] Initiating Mongo Client")
  result = MongoClient(host, port)
  if result.server_info()["ok"] == 1.0:
    print("\tClient Initiated")
  return result

def initContainer(port, username, password, container_name):
  command = "$ docker run -e MONGO_INITDB_ROOT_USERNAME=%s -e MONGO_INITDB_ROOT_PASSWORD=%s" % (
    username,
    password
  )
  command = "%s -d -p %d:27017 --name %s mongo --auth" % (command, port, container_name)
  print("[x] Create MongoDb container\n%s" % command)
  input()

def loadConfiguration():
  file_path = path.join(
    path.dirname(__file__),
    "config.json"
  )
  with open(file_path, "r") as read_file:
    result = load(read_file)
  return result

def doesUserExist(db, username):
  if db.command("usersInfo", usersInfo=username)['users']:
    return True
  else:
    return False
