import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL")

if BASE_API_URL is None:
    print("Error: BASE_API_URL not set in the .env file.")
    exit()

url = f"{BASE_API_URL}/detail_pengumpulan"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    formatted_data = json.dumps(data, indent=2)
    print(formatted_data)
else:
    print(f"Error: {response.status_code} - {response.text}")
