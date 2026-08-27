import io
import base64

import requests
import matplotlib
matplotlib.use("Agg")  # no GUI backend needed on a server
import matplotlib.pyplot as plt

from django.shortcuts import render

COINS = "bitcoin,ethereum,solana,dogecoin"
CURRENCY = "usd"
URL = f"https://api.coingecko.com/api/v3/simple/price?ids={COINS}&vs_currencies={CURRENCY}"


def fetch_prices():
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
    coins = list(data.keys())
    prices = [data[coin][CURRENCY] for coin in coins]
    return coins, prices


def make_pie_chart(coins, prices):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(prices, labels=coins, autopct="%1.1f%%", startangle=90)
    ax.set_title("Price Share (USD)")

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def index(request):
    chart_image = None
    error = None

    if "fetch" in request.GET:
        try:
            coins, prices = fetch_prices()
            chart_image = make_pie_chart(coins, prices)
        except requests.exceptions.RequestException:
            error = "Couldn't fetch prices right now. Try again in a moment."

    return render(request, "charts/index.html", {
        "chart_image": chart_image,
        "error": error,
    })