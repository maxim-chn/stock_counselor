from json import dumps
from traceback import format_exc

class ApplicativeUser:
  """
  Represents a user who uses the application, for example a human.
  """
  class_name = "ApplicativeUser"
  max_error_chars = 1000

  def __init__(self):
    self._first_name = None
    self._last_name = None
    self._user_id = None

  @classmethod
  def applicativeUserWith(cls, first_name, last_name, user_id):
    """
    Returns ApplicativeUser.
    Raises RuntimeError.
    Arguments:
      - first_name -- str.
      - last_name -- str.
      - user_id -- str. It is an email address.
    """
    try:
      result = cls()
      result.first_name = first_name
      result.last_name = last_name
      result.user_id = user_id
      return result
    except RuntimeError as err:
      err_msg = "%s -- applicativeUserWith -- Failed.\n%s" % (ApplicativeUser.class_name, str(err))
      raise RuntimeError(err_msg)

  @classmethod
  def fromDocument(cls, val):
    """
    Returns ApplicativeUser.
    Raises RuntimeError.
    Arguments:
      - val -- dict.
    """
    try:
      first_name = val["first_name"]
      last_name = val["last_name"]
      user_id = val["user_id"]
      result = cls.applicativeUserWith(first_name, last_name, user_id)
      return result
    except RuntimeError as err:
      err_msg = "%s -- fromDocument -- Failed.\n%s" % (ApplicativeUser.class_name, str(err))
      raise RuntimeError(err_msg)
    except Exception as err:
      err_msg = "%s -- fromDocument -- Failed.\n%s" % (
        ApplicativeUser.class_name, format_exc(ApplicativeUser.max_error_chars, err)
      )
      raise RuntimeError(err_msg)

  def toDocument(self):
    """
    Returns dict.
    """
    result = {
      "first_name": self.first_name,
      "last_name": self.last_name,
      "user_id": self.user_id
    }
    return result

  def toJson(self):
    """
    Returns str.
    Raises RuntimeError.
    """
    try:
      return dumps(self.toDocument())
    except Exception as err:
      err_msg = "%s -- toJson -- Failed.\n%s" % (self._class_name, format_exc(self.max_error_chars, err))
      raise RuntimeError(err_msg)

  def __str__(self):
    """
    Returns str.
    """
    return str(self.toDocument())
  
  # Getters and setters
  
  @property
  def first_name(self):
    """
    Returns str or None.
    """
    return self._first_name

  @property
  def last_name(self):
    """
    Returns str or None.
    """
    return self._last_name

  @property
  def user_id(self):
    """
    Returns str or None.
    """
    return self._user_id

  @first_name.setter
  def first_name(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - val -- str.
    """
    if val and isinstance(val, str):
      self._first_name = val
    else:
      raise RuntimeError("%s -- first_name -- setter expected a non-empty str." % ApplicativeUser.class_name)

  @last_name.setter
  def last_name(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - val -- str.
    """
    if val and isinstance(val, str):
      self._last_name = val
    else:
      raise RuntimeError("%s -- last_name -- setter expected a non-empty str." % ApplicativeUser.class_name)

  @user_id.setter
  def user_id(self, val):
    """
    Returns void.
    Raises RuntimeError.
    Arguments:
      - val -- str. An email address.
    """
    if val and isinstance(val, str) and "@" in val and "." in val:
      self._user_id = val
    else:
      raise RuntimeError("%s -- user_id -- setter expected an email address." % ApplicativeUser.class_name)
