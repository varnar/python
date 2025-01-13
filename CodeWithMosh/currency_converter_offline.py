# This is a simple offline currency converter that converts from one currency to another
# using a fixed exchange rate. The exchange rates are stored in a dictionary.
#
# The user is prompted to enter the amount they want to convert, the source currency,
# and the target currency. The program then calculates the converted amount using the
# exchange rate and displays the result.
#
# The exchange rates are stored in a dictionary called exchange_rate, where the keys are
# the target currencies and the values are the exchange rates. The exchange_rate_list
# variable is a list of the target currencies for display purposes.
#
# The get_amount function prompts the user to enter the amount they want to convert and
# validates the input to ensure it is a positive number.
#
# The get_currency function prompts the user to enter the source or target currency and
# validates the input to ensure it is a valid currency code.
#
# The convert_currency function takes the amount, source currency, and target currency as
# input and calculates the converted amount using the exchange rate.
#
# The main function is the entry point of the program. It calls the get_amount and
# get_currency functions to get the user input and then calls the convert_currency function
# to calculate the converted amount. Finally, it displays the result to the user.
#
# To run the program, simply execute the script. The user will be prompted to enter the amount,
# source currency, and target currency. The program will then display the converted amount.
#
# Example:
# Enter the amount you want to convert from: 100
# == Source exchange currency list: ['USD', 'EUR', 'GBP']
# Source currency: USD
# == Target exchange currency list: ['EUR', 'GBP']
# Target currency: EUR
# 100.0 USD is equal to 85.0 EUR

exchange_rate = {
    "USD": 1,
    "EUR": 0.85,
    "CAD": 1.4431
    }

exchange_rate_list = list(exchange_rate.keys())

# Function to get the amount to convert
def get_amount():
    while True:
        try:
            amount = float(input("Enter the amount you want to convert from: "))
            if amount <= 0:
                raise ValueError
        except ValueError:
            print("Please enter a valid number")
            continue
        return amount

# Function to get the source or target currency
def get_currency(exchange_rate_list,label):
    print(f"== {label.capitalize()} exchange curenncy list: {exchange_rate_list}")
    while True:
        currency = input(f"{label.capitalize()} currency: ").upper()
        if currency not in exchange_rate_list:
            print("Please enter a valid currency")
            continue
        return currency

# Function to convert the amount from the source currency to the target currency
def convert_currency(amount, source_currency, target_currency):
    converted_amount = amount * exchange_rate[target_currency] / exchange_rate[source_currency]
    return converted_amount

# Main function
def main():
    amount = get_amount()
    source_currency = get_currency(exchange_rate_list,"source")
    target_currency = get_currency(exchange_rate_list,"target")
    converted_amount = convert_currency(amount, source_currency, target_currency)
    print(f"{amount} {source_currency} is equal to {converted_amount} {target_currency}")

# Run the program
if __name__ == "__main__":
    main()