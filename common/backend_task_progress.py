from enum import Enum

class BackendTaskProgress(Enum):
  FAILED_TO_UPDATE_PROGRESS = "Task Progress Update has Failed"
  FINISHED = "Task has been Completed"
  STARTED = "Task has been Initiated"
  QUERYING_FOR_10K_REPORT_CONTENTS = "Looking for the 10-K Report Contents at the SEC website"
  QUERYING_FOR_10K_IDS = "Looking for Company 10-K Report Ids at the SEC website"
  QUERYING_FOR_AVAILABLE_10K_REPORTS = "Looking for the Available Company 10-K Reports at the SEC website"
  QUERYING_FOR_10K_REPORT = "Looking for the Company 10-K Report at the SEC website"
  QUERYING_FOR_COMPANY_ID = "Looking for the Company Id at the SEC website"
  QUERYING_FOR_FINANCIAL_STMNT_CONTENTS = "Looking for the Financial Statement Contents at the SEC website"
  QUERYING_FOR_FINANCIAL_STMNT_TYPES = "Looking for Company 10-K Financial Statements Types at the SEC website"
  UPDATED_PROGRESS = "Task Progress has been Updated"
