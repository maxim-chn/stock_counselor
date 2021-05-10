from os import path
from json import load
import pika

def createAllUsers(users):
  for user in users:
    command = "$ rabbitmqctl add_user %s %s" % (user["username"], user["password"])
    print("[x] Create User %s \n%s" % (user["username"], command))
    input()

def dropAllUsers(usernames):
  for username in usernames:
    command = "$ rabbitmqctl delete_user %s" % username
    print("[x] Delete User %s \n%s" % (username, command))
    input()

def grantPermissions(user_permissions):
  for permissions in user_permissions:
    command = "$ rabbitmqctl set_permissions -p \"%s\" %s " % (permissions["vhost"], permissions["username"])
    command += "\"%s|%s\"" % (permissions["exchange"], permissions["queue"])
    command += " \"%s|%s\"" % (permissions["exchange"], permissions["queue"])
    command += " \"%s|%s\"" % (permissions["exchange"], permissions["queue"])
    print("[x] Set permissions for %s\n%s" % (permissions["username"], command))
    input()

def initContainer(host, server_port, ui_port, container_name, username, password, release, line_separator):
  command = "$ docker run -d --hostname %s -p %s:5672 -p %s:15672 %s\n" % (
    host, server_port, ui_port, line_separator
  )
  command += " --name %s -e RABBITMQ_DEFAULT_USER=%s -e RABBITMQ_DEFAULT_PASS=%s %s\n" % (
    container_name, username, password, line_separator
  )
  command += " rabbitmq:%s" % release
  print("[x] Create RabbitMQ container\n%s" % command)
  input()

def sendMessage(user, connection):
  print("[x] Checking the %s queue" % user["channel"]["name"])
  credentials = pika.PlainCredentials(user["username"], user["password"])
  parameters = pika.ConnectionParameters(connection["host"],
                                         connection["server_port"],
                                         connection["vhost"],
                                         credentials)

  connection = pika.BlockingConnection(parameters)
  channel = connection.channel()
  response = channel.queue_declare(user["channel"]["name"])
  channel.queue_bind(exchange=user["channel"]["exchange"], queue=response.method.queue)
  channel.basic_publish(exchange=user["channel"]["exchange"], routing_key=user["channel"]["name"], body="Hello")
  connection.close()

def receiveMessage(user, connection):
  credentials = pika.PlainCredentials(user["username"], user["password"])
  parameters = pika.ConnectionParameters(connection["host"],
                                         connection["server_port"],
                                         connection["vhost"],
                                         credentials)

  connection = pika.BlockingConnection(parameters)
  channel = connection.channel()
  channel.queue_declare(queue=user["channel"]["name"])
  def callback(ch, method, properties, body):
    if "Hello" in str(body):
      print("[X] %s queue is active" % user["channel"]["name"])
    else:
      print("%s queue is corrupted" % user["channel"]["name"])
    ch.stop_consuming()
  channel.basic_consume(queue=user["channel"]["name"], auto_ack=True, on_message_callback=callback)
  channel.start_consuming()
  connection.close()




def initializeRabbitMq(os):
  config = loadConfiguration()
  initContainer(
    config["connection"]["host"],
    config["connection"]["server_port"],
    config["connection"]["ui_port"],
    config["container"]["name"],
    config["users"]["root"]["username"],
    config["users"]["root"]["password"],
    config["container"]["release"],
    config["line_separator"][os]
  )
  usernames = [
    config["users"]["data_gatherer_main"]["username"],
    config["users"]["data_gatherer_worker"]["username"],
    config["users"]["recommendation_main"]["username"],
    config["users"]["recommendation_worker"]["username"]
  ]
  dropAllUsers(usernames)
  users = [
    config["users"]["data_gatherer_main"],
    config["users"]["data_gatherer_worker"],
    config["users"]["recommendation_main"],
    config["users"]["recommendation_worker"]
  ]
  createAllUsers(users)
  permissions = [
    config["permissions"]["data_gatherer_main"],
    config["permissions"]["data_gatherer_worker"],
    config["permissions"]["recommendation_main"],
    config["permissions"]["recommendation_worker"]
  ]
  grantPermissions(permissions)
  sendMessage(
    config["users"]["data_gatherer_main"],
    config["connection"]
  )
  receiveMessage(
    config["users"]["data_gatherer_worker"],
    config["connection"]
  )
  sendMessage(
    config["users"]["recommendation_main"],
    config["connection"]
  )
  receiveMessage(
    config["users"]["recommendation_worker"],
    config["connection"]
  )


def loadConfiguration():
  file_path = path.join(
    path.dirname(__file__),
    "rabbitmq.json"
  )
  with open(file_path, "r") as read_file:
    result = load(read_file)
  return result
