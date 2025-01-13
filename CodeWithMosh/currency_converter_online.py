import requests

# Replace with your actual API key
API_KEY = '08906ffe6c7ad809aa8deef6'
BASE_URL = 'https://v6.exchangerate-api.com/v6/'

# Fetch exchange rate from the API

def get_exchange_rate(api_key, base_currency, target_currency):
    url = f"{BASE_URL}{api_key}/latest/{base_currency}"
    print(f"Fetching exchange rate from {url}...")
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        raise Exception(f"Error fetching exchange rate: {data['error-type']}")
    return data['conversion_rates'][target_currency]

# Convert the amount from the base currency to the target currency
def convert_currency(amount, base_currency, target_currency):
    exchange_rate = get_exchange_rate(API_KEY, base_currency, target_currency)
    print(f"Exchange rate: {exchange_rate}")
    return amount * exchange_rate

# Entry point of the program
def main():
    amount = float(input("Enter amount: "))
    base_currency = input("Enter base currency (e.g., USD): ").upper()
    target_currency = input("Enter target currency (e.g., EUR): ").upper()
    try:
        converted_amount = convert_currency(amount, base_currency, target_currency)
        print(f"{amount} {base_currency} is equal to {converted_amount:.2f} {target_currency}")
    except Exception as e:
        print(e)

# Run the program
if __name__ == "__main__":
    main()