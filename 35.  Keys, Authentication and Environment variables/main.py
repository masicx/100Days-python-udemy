import requests, json
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")
API_URL = os.environ.get("API_URL")
PASSWORD = str(os.environ.get("EMAIL_PASSWORD"))
EMAIL_TO = str(os.environ.get("EMAIL_TO"))

# parameters = {"lat": 19.243919, "lon": -103.728539, "appid": API_KEY, "lang": "es"}
# response = requests.get(API_URL, params=parameters)
# print(response.status_code)
# print(response.json())

def send_email(message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="masicx@gmail.com", password=PASSWORD)
        connection.sendmail(
            from_addr="masicx@gmail.com", 
            to_addrs=EMAIL_TO, 
            msg=f"Subject: Hello\n\n{message}")

with open(r"C:\Code\100DaysCourse\35.  Keys, Authentication and Environment variables\response.json", "r") as file:
    json_data = json.load(file)

will_rain = False
for hour_data in json_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    send_email("Bring an umbrella")