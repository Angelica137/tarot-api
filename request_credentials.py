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

