import requests

COINS = "bitcoin,ethereum"
CURRENCY = "usd"

URL = f"https://api.coingecko.com/api/v3/simple/price?ids={COINS}&vs_currencies={CURRENCY}"


def main():
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()

    for coin, prices in data.items():
        print(f"{coin}: {prices[CURRENCY]} {CURRENCY.upper()}")


if __name__ == "__main__":
    main()