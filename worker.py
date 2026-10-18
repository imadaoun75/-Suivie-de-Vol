import os
import time
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration (via variables d'environnement)
AVIATIONSTACK_KEY = os.getenv("AVIATIONSTACK_KEY")
SMSGATE_API_URL = os.getenv("SMSGATE_API_URL")
SMSGATE_TOKEN = os.getenv("SMSGATE_TOKEN")
# Note : Pour Outlook/Microsoft Graph, la configuration est plus complexe
# (nécessite une App Registration Azure avec OAuth2)

def get_flights_from_outlook():
    # TODO: Implémenter la logique de lecture du calendrier via Microsoft Graph API
    return []

def get_flight_status(flight_number):
    # Appel à l'API AviationStack
    url = f"http://api.aviationstack.com/v1/flights?access_key={AVIATIONSTACK_KEY}&flight_iata={flight_number}"
    response = requests.get(url)
    return response.json()

def send_sms_notification(message):
    # Appel à votre service SMSGate
    payload = {"token": SMSGATE_TOKEN, "message": message}
    requests.post(SMSGATE_API_URL, data=payload)

def monitor():
    print("Démarrage du moniteur de vols...")
    while True:
        flights = get_flights_from_outlook()
        for flight in flights:
            status = get_flight_status(flight['number'])
            # Logique pour comparer avec le statut précédent
            # Si changement -> send_sms_notification(...)
        
        # Attendre avant la prochaine vérification (ex: toutes les 30 minutes)
        time.sleep(1800)

if __name__ == "__main__":
    monitor()
