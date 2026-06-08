class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, price: float, origin_airport: str, destination_airport: str, out_date: str, return_date: str):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date