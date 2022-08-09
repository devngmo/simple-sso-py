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

## create sample apis:
- [/]: return text 'welcome'
- [/object/__{category}__]: return a Json model of basic information for an object in __category__

## first run:
- Run web api with command:
```python -m uvicorn main:app```

- Open browser with url: (http://localhost:8000/docs)[http://localhost:8000/docs]

## release version 0.0.1

### * create docker image for version 0.0.1

