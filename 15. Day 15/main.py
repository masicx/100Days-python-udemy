MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0,
}

def print_report():
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${resources['money']}")

def check_resources(drink):
    for item in drink["ingredients"]:
        if resources[item] < drink["ingredients"][item]:
            print(f"Sorry, there is not enough {item}.")
            return False
    return True

def process_coins():
    print("Please insert coins.")
    quarters = int(input("How many quarters?: "))
    dimes = int(input("How many dimes?: "))
    nickels = int(input("How many nickels?: "))
    pennies = int(input("How many pennies?: "))
    total = quarters * 0.25 + dimes * 0.10 + nickels * 0.05 + pennies * 0.01
    return total

user_input = ""
while user_input != "off":
    user_input = input("What would you like? (espresso/latte/cappuccino): ").lower()
    if user_input == 'report':
        print_report()
    elif user_input in MENU:
        drink = MENU[user_input]
        if not check_resources(drink):
            continue
        coin_value = process_coins()
        if coin_value < drink["cost"]:
            print("Sorry, that's not enough money. Money refunded.")
        else:
            resources["money"] += drink["cost"]
            change = round(coin_value - drink["cost"], 2)
            print(f"Here is ${change} in change.")
            for item in drink["ingredients"]:
                resources[item] -= drink["ingredients"][item]
            print(f"Here is your {user_input}. Enjoy!")
    elif user_input == "off":
        print("Shutting down the machine. Goodbye!")
    else:
        print("Invalid input. Please try again.")