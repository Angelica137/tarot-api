import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUDIENCE = os.getenv("API_AUDIENCE")

url = f"https://{AUTH0_DOMAIN}/oauth/token"
headers = {"content-type": "application/json"}
payload = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "audience": AUDIENCE,
    "grant_type": "client_credentials"
}

response = requests.post(url, json=payload, headers=headers)
token = response.json().get("access_token")

print(f"Token: {token}")


eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZsSzhSSFFiV2NwalFWNGhEWFVGcSJ9.eyJpc3MiOiJodHRwczovL2Rldi1xMnpqbmFucHo4ZWd6emtiLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJHNjZHWllOTXB2WTlyOEVrTDUxSXBxTUVhVVozUUUxRUBjbGllbnRzIiwiYXVkIjoiaHR0cDovLzEyNy4wLjAuMTo1MDAwL2FwaS8iLCJpYXQiOjE3MjEwODYyMzgsImV4cCI6MTcyMTE3MjYzOCwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwiYXpwIjoiRzY2R1pZTk1wdlk5cjhFa0w1MUlwcU1FYVVaM1FFMUUiLCJwZXJtaXNzaW9ucyI6W119.1x02y9LcVzrbtDyltMY5jmSkK03kPN7zT3cHG2Q3FMsGgUQIkt8z9uJvGA1zZF2idKKopjiZlsR9B7uVCeU_oxVOIaVrZN6kZwq_DrB_4aX4wODjhfiPMtlUaH2hz3TuGWAKNQueNPCQKLp3b7uX6XaELOL4Fyx6wI0Xq-2UIAqnCB67HEYRUzeOjsvAXQ8qA3QbJmFFL_2O5hmGKQhb1fadMw3GXTKr0mLz5acHHVh7fzSmhtax1_n6NbUFW9ZbHSX-3yZc-zdBlwd7g-QNfLHwcAWnVXSLxcfnOyy8mV2Ejw8_YPY9v1sC-f4Y784xqw3BE8Jp2i2z4n78I4V3Tg