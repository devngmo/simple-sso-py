@cls

set API_ENDPOINT_EMAIL_CONFIRM=http://127.0.0.1:8000
set HOST_IP=127.0.0.1
set HOST_PORT=8000
set GMAIL_ACCOUNT=test@gmail.com
set GMAIL_APP_PASSWORD=1231231231232133
cd app
python -m uvicorn main:app --host %HOST_IP% --port %HOST_PORT%