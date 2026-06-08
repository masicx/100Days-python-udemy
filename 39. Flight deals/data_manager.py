import requests
from dotenv import load_dotenv
import os

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        load_dotenv()
        self.sheety_auth = os.getenv("SHEETY_AUTH")
        self.headers = {
            "Authorization": f"Basic {self.sheety_auth}"
        }

    def get_destination_data(self):
        response = requests.get(url="https://api.sheety.co/1dd196c88ac7b4381b4da5ffb60d6724/flightDeals/prices", headers=self.headers)
        data = response.json()
        return data["prices"]
    
    def update_destination_codes(self, id: int, iata_code: str, city: str, lowest_price: float):
        body = {
            "price": {
                "iataCode": iata_code,
                "city": city,
                "lowestPrice": lowest_price
            }
        }

        response = requests.put(url=f"https://api.sheety.co/1dd196c88ac7b4381b4da5ffb60d6724/flightDeals/prices/{id}", json=body, headers=self.headers)
        response.raise_for_status()
        print(response.text)