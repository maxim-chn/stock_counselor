# stock-counselor
This is a counselor for the Stock Investment based on the Fundamental Approach

# MongoDB Container
## Initialization (Windows OS)
**(1)** Build the *stock_counselor_image* with
```
docker build -t stock_counselor_image ./docker_image
```

**(2)** Execute the *windows_os.ps1* script with an option to bypass security policy
```
powershell -ExecutionPolicy Bypass -File .\windows_os.ps1
```