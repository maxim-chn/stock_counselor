
class InvalidCredentialsError(RuntimeError):

  MIN_FIRST_NAME_LENGTH = 3
  MIN_LAST_NAME_LENGTH = 2

  def __init__(self, message):
    super().__init__(message)
