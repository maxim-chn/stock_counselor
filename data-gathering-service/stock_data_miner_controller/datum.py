"""
This is an input for the states

"""


class Datum:
  def __init__(self, name, value):
    self._name = name
    self._inputs = []
    self._value = value


  def addInput(self, datum):
    self._inputs.append(datum)

  def getDatum(self, name):
    value = None
    for x in self._inputs:
      if x.getName() == name:
        value = x
      break

    return value

  def getName(self):
    return self._name

  def dateValue(self):
    return datetime.strptime(self._value)

  def integerValue(self):
    return int(self._value)

  def stringValue(self):
    return self._value

    

