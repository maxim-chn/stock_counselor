from enum import Enum

class BackendTaskProgress(Enum):
  FAILED_TO_UPDATE_PROGRESS = "Task Progress Update has Failed"
  FINISHED = "Task has been Completed"
  STARTED = "Task has been Initiated"
  UPDATED_PROGRESS = "Task Progress has been Updated"
