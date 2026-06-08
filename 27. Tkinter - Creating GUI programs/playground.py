# Unlimited positional arguments
def add(*args):
    total = 0
    for n in args:
        total += n
    return total


# print(add(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))


# Unlimited keyword arguments
def calculate(n, **kwargs):
    print(kwargs)
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)


# calculate(2, add=3, multiply=5)

class Car():
    def __init__(self, **kw):
        """Initialize the car

        Args:
            **kw: Keyword arguments for the car

        Keyword Arguments:
            make {str} -- The make of the car (default: {None})
            model {str} -- The model of the car (default: {None})

        Returns:
            Car - A car
        """
        self.make = kw.get("make")
        self.model = kw.get("model") # If the key doesn't exist, return None

my_car = Car(make="Nissan")
print(my_car.make)
print(my_car.model)
