import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_KEY = os.getenv("AVIATIONSTACK_KEY")
SMSGATE_API_URL = os.getenv("SMSGATE_API_URL")
SMSGATE_TOKEN = os.getenv("SMSGATE_TOKEN")

FLIGHTS_FILE = os.getenv("FLIGHTS_FILE", "vols.json")
CHECK_INTERVAL = 1800  # 30 minutes
previous_statuses = {}


def load_flights():
    try:
        with open(FLIGHTS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("vols", [])
    except FileNotFoundError:
        print(f"Fichier introuvable : {FLIGHTS_FILE}")
    except (json.JSONDecodeError, OSError) as error:
        print(f"Impossible de lire {FLIGHTS_FILE} : {error}")
    return []


def get_flight_status(flight_number):
    if not AVIATIONSTACK_KEY:
        print("Variable AVIATIONSTACK_KEY manquante.")
        return None

    url = "http://api.aviationstack.com/v1/flights"
    try:
        response = requests.get(
            url,
            params={
                "access_key": AVIATIONSTACK_KEY,
                "flight_iata": flight_number,
            },
            timeout=30,
        )
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[0] if data else None
    except (requests.RequestException, ValueError) as error:
        print(f"Erreur lors de la vérification de {flight_number} : {error}")
        return None


def send_sms_notification(message, phone):
    if not SMSGATE_API_URL or not SMSGATE_TOKEN:
     
