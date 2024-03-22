import time
from data_file import prices, ingredients, resources, options


def main():
    while enough_for_one_more_coffee():
        intro()
        choice = check_choice(input("Please select an option: ").lower())
        if choice == "report":
            print_resources()
        elif choice == "done":
            print("Java Nice Day!")
            quit()
        else:
            if ingredients_for_coffee(choice):
                coins_inserted = insert_coins(choice)
                if coins_inserted >= prices[choice]:
                    print(f"Entered £{coins_inserted:.2f} | Your change is: £{(coins_inserted - prices[choice]):.2f}")
                    hand_coffee_reduce_resources(choice)
    print("Warning! Not enough ingredients to make coffee. Please refill tank.")


def enough_for_one_more_coffee():
    return resources["coffee"] >= 18 and resources["water"] >= 50


def ingredients_for_coffee(option):
    not_enough = False
    for key in ingredients[option]:
        if ingredients[option][key] > resources[key]:
            print(f"Not enough {key} to make {option}!")
            not_enough = True
    if not_enough:
        print("Please select a different option.\n")
        return False
    else:
        return True


def hand_coffee_reduce_resources(option):
    print("\nPreparing coffee...")
    time.sleep(3)
    print(f"Enjoy your {option}!\n")
    for key in ingredients[option]:
        resources[key] -= ingredients[option][key]


def intro():
    print("Coffees: Espresso / Latte / Capuccino")
    print("Select 'report' for remaining ingredients. Select 'done' to exit.")


def print_resources():
    print("\nRemaining ingredients")
    for ingredient, amount in resources.items():
        if ingredient != "coffee":
            print(f"{ingredient.capitalize()}: {amount}ml")
        else:
            print(f"{ingredient.capitalize()}: {amount}g")
    print()


def check_choice(request):
    if request not in options:
        return check_choice(input("Invalid option. Select a valid option: ").lower())
    else:
        return request


def insert_coins(option):
    coins_entered = 0
    coins = [0.01, 0.02, 0.05, 0.1, 0.20, 0.50, 1, 2]
    while coins_entered < prices[option]:
        print(f"\n{option}: cost: £{prices[option]:.2f}")
        print(f"Amount entered: £{coins_entered:.2f}")
        coin = input("Select 'back' or Insert coins: £")
        if coin == "back":
            print(f"\nPayment cancelled. Here is your change: £{coins_entered:.2f}")
            return coins_entered
        else:
            coin = convert_float(coin)
            if coin not in coins:
                print("Invalid coin!\n")
            else:
                coins_entered += coin
    return coins_entered


def convert_float(coin):
    try:
        return float(coin)
    except (ValueError, TypeError):
        return convert_float(input("Please enter following coins only: (1p, 2p, 5p, 10p, 20p, 50p, £1, £2"))


main()
