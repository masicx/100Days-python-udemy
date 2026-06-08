import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")
API_ID = os.environ.get("API_ID")
API_URL = "https://app.100daysofpython.dev"

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY
}

exercise = input("What exercise did you do? ")
weight_kb = 103
height_cm = 172
age = 35

parameters = {
    "query": exercise,
    "gender": "male",
    "weight_kg": weight_kb,
    "height_cm": height_cm,
    "age": age
}

response = requests.post(url=API_URL + "/v1/nutrition/natural/exercise", json=parameters, headers=headers)
response.raise_for_status()
data = response.json()["exercises"][0]

workout_endpoint = "https://api.sheety.co/1dd196c88ac7b4381b4da5ffb60d6724/myWorkouts/workouts"
workout={
    "workout": {
        "date": datetime.now().strftime("%d/%m/%Y"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "exercise": data["name"].title(),
        "duration": data["duration_min"],
        "calories": data["nf_calories"]
    }
}
workout_headers = {
    "Authorization": f"Basic {os.environ.get('SHEETY_AUTH')}"
}

workout_response = requests.post(url=workout_endpoint, json=workout, headers=workout_headers)
workout_response.raise_for_status()

print(workout_response.text)
