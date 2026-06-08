import requests
from datetime import datetime

parameters = {"lat": 19.243919, "lng": -103.728539, "formatted": 0}
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status
data = response.json()

hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
print(hour)
print(data["results"]["sunset"])
time_now = datetime.now()
print(time_now.hour)