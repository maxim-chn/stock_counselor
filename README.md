# stock-counselor
This is a counselor for the Stock Investment based on the Fundamental Approach

# Prerequisites
- OS: Windows 10
- Powershell
- WSL 2 with Ubuntu 20.04
- Docker
- Python 3.x

# Initialization steps

**(1)** Execute the *windows_os.ps1* script with an option to bypass security policy
```
powershell -ExecutionPolicy Bypass -File .\windows_os.ps1
```

**(2)** Validate that *mongo_local* and *rabbitmq_local* containers have been created and are running.

**(3)** Validate that a directory *.venv* has been created

# Service start
There are 4 services in total:
  - data_gathering_main_service
  - data_gathering_worker_service
  - recommendation_main_service
  - recommendation_worker_service

To start a service, execute the *run.ps1* script with a service name as an argument and
an option to bypass security policy. For example
```
powershell -ExecutionPolicy Bypass -File .\run.ps1 "data_gathering_main_service"
```