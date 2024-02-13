import CoffeeMachineInfo
from CoffeeMachineInfo import coffee_options, coffee_req, resources
import time


def main():
    # play the intro
    intro()
    # check there's at least enough in the machine to deliver one more coffee
    while enough_for_one_more():
        try:
            coffee_choice = input("Please enter a coffee: ").lower()
        # if user does ctrl + d/c then exit gracefully without traceback
        except (EOFError, KeyboardInterrupt):
            print("Thank you for drinking with us today!")
            quit()
        # check if the coffee requested is actually an option - if not, alert the user and get input again
        if is_an_option(coffee_choice, coffee_options):
            pass
        else:
            continue
        # if the option is report - show remaining resources, if the option is done - end the program
        if coffee_choice == "report":
            report()
            continue
        elif coffee_choice == "done":
            done()
        # check that there are enough resources for the coffee - if no, tell the user,
        # if yes - give coffee and subtract the resource-cost from resources
        if check_resources(coffee_choice):
            amount = get_coffee_price(coffee_choice)
            cents, nickels, dimes, quarters = get_coins()
            inserted_coins = cents + nickels + dimes + quarters
            if compare_amount(amount, inserted_coins):
                CoffeeMachineInfo.resources = hand_coffee(coffee_choice)
                resources["Money"] += amount
            else:
                continue
        else:
            print(CoffeeMachineInfo.resources)

def intro():
    try:
        print("Welcome to the coffee machine")
        time.sleep(2)
        print("Your coffee options are: espresso, latte and cappuccino")
        time.sleep(3)
        print("(type \"report\" for remaining resources and \"done\" to exit coffee machine)")
        time.sleep(3)
    except (EOFError, KeyboardInterrupt):
        print("Thank you for drinking with us today!")
        quit()


def enough_for_one_more():
    if coffee_req[0]["water"] > resources["water"] or coffee_req[0]["coffee"] > resources["coffee"]:
        print("Not enough for any more coffees, thank you for ordering with us today!")
        return quit()
    else:
        return True


def check_resources(user_input):
    for i in range(len(coffee_req)):
        if user_input == coffee_req[i]["name"]:
            coffee_index = i

    verdict = ""
    if coffee_req[coffee_index]["water"] > resources["water"]:
        print("not enough water")
        verdict = "not enough"
    if coffee_req[coffee_index]["coffee"] > resources["coffee"]:
        print("not enough coffee")
        verdict = "not enough"
    if coffee_req[coffee_index]["milk"] > resources["milk"]:
        print("not enough milk")
        verdict = "not enough"

    if verdict == "not enough":
        return False
    else:
        return True


def hand_coffee(user_input):
    for i in range(len(coffee_req)):
        if user_input == coffee_req[i]["name"]:
            index = i
            hand_coffee = coffee_req[i]["name"]
            print(f"Here you go, enjoy your {hand_coffee}!")

    resources["water"] -= coffee_req[index]["water"]
    resources["milk"] -= coffee_req[index]["milk"]
    resources["coffee"] -= coffee_req[index]["coffee"]

    return resources


def report():
    for key, value in resources.items():
        if key == "Money":
            print(key, f"${value:.2f}")
        else:
            print(key, value)


def done():
    print("Thank you for drinking with us today!")
    quit()


def is_an_option(request, items):
    if request not in items:
        print("Not an option, please try again!")
        return False
    else:
        return True


def get_coffee_price(coffee_choice):
    coffee_prices = {"espresso": 2.25, "cappuccino": 2.50, "latte": 3.50}
    # while coffee_choice not in coffee_prices:
    #     coffee_choice = input("Not an option please, choose a valid coffee.")
    for coffee in coffee_prices:
        if coffee == coffee_choice:
            coffee_price = round(coffee_prices[coffee], 2)
            print(coffee, f"price: £{coffee_price:.2f}")
            return coffee_price


def get_coins():
    while True:
        try:
            cents = int(input("Enter your number of cents: "))
            nickels = int(input("Enter your number of nickels: "))
            dimes = int(input("Enter your number of dimes: "))
            quarters = int(input("Enter your number of quarters: "))
            cents *= 0.01
            nickels *= 0.05
            dimes *= 0.10
            quarters *= 0.25
            return cents, nickels, dimes, quarters
        except ValueError:
            print("Invalid input, please enter numeric values only")
        except (KeyboardInterrupt, EOFError):
            print("Thank you for drinking with us today!")
            quit()


def compare_amount(amount, inserted_coins):
    if inserted_coins < amount:
        print(f"Too little amount entered - please receive your change: ${inserted_coins:.2f}")
        return False
    elif inserted_coins == amount:
        return True
    else:
        change = inserted_coins - amount
        print(f"Here is your change: ${change:.2f}")
        return True


main()
