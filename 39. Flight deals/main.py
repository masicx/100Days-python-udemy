from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.


data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6*30))

flight_search = FlightSearch()

for destination in sheet_data:
    flight = flight_search.check_flights(
        origin_city_code="LON",
        destination_city_code=destination["iataCode"],
        from_time=tomorrow.strftime("%Y-%m-%d"),
        to_time=six_month_from_today.strftime("%Y-%m-%d")
    )
    print(flight)