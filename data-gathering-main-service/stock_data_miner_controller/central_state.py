"""
manages state-machine
collects data from states
"""

class CentralState:
  """
  dataset - Datum
  result - dictionary
  states - list<<State>>
  """
  def __init__(self, dataset):
    self._dataset = dataset
    self._result = dict()
    self._states = []


  def executeFlow(self):
    pass



