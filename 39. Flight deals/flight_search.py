
from dotenv import load_dotenv
import requests
import os
# x-app-id: 
# x-app-key:


BASE_URL = "https://app.100daysofpython.dev"
API_ENDPOINT = "/v1/flights/search"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        load_dotenv()

        # Provide empty-string defaults so header values are always str (avoids type errors)
        self.app_id = os.getenv("FLIGHT_APP_ID", "")
        self.app_key = os.getenv("FLIGHT_APP_KEY", "")

    def check_flights(self, origin_city_code: str, destination_city_code: str, from_time: str, to_time: str):
        headers = {
            "x-app-id": self.app_id,
            "x-app-key": self.app_key
        }

        query = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time,
            "return_date": to_time,
            "type": "1",
            "adults": "1",
            "currency": "GBP",
            "api_key": self.app_key
        }

        response = requests.get(url=f"{BASE_URL}{API_ENDPOINT}", headers=headers, params=query)
        response.raise_for_status()
        return response.json()

