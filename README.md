# stock-counselor
This is a counselor for the Stock Investment based on the Fundamental Approach

# Prerequisites
- OS: Windows 10
- OS features: WSL 2 with Ubuntu 20.04
- Docker

# Initialization steps

**(1)** Execute the *windows_os.ps1* script with an option to bypass security policy
```
powershell -ExecutionPolicy Bypass -File .\windows_os.ps1
```
**(2)** Validate that containers "mongo_local" and "rabbitmq_local" have been created and are running.