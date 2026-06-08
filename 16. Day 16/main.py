from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

def report():
    coffee_maker.report()
    money_machine.report()

user_input = ""
while user_input != "off":
    user_input = input(f"What would you like? ({menu.get_items()}): ")
    if user_input == "report":
        report()
    else:
        drink = menu.find_drink(user_input)
        if drink and coffee_maker.is_resource_sufficient(drink):
            if money_machine.make_payment(drink.cost):
                coffee_maker.make_coffee(drink)


        