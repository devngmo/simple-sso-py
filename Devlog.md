# Devlog
Records everything I did while coding this project.

====================================
# You Need: Run CMD or PowerShell as Administrator
====================================
## - Upgrade pip
```
python.exe -m pip install --upgrade pip
```

## - Install Fast API
Requirements: you already install python and pip.

```
pip install fastapi
```
## - Install uvicorn
To run as a production server
```
pip install uvicorn[standard]
```

## create api for register:
- [/register]: accept body as RegistrationModel, send confirm email to user.
- [/register/validate/{token}]: validate token ( when user click on confirm link in email ) and activate account if token not expired.

## first run:
- Run web api with command:
    - exec file: ```run.bat```

- Open browser with url: (http://localhost:8000/docs)[http://127.0.0.1:8000/docs]

## release version 0.0.1

### * create docker image for version 0.0.1

