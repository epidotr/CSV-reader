import io
import base64
from datetime import datetime

import requests
import matplotlib
matplotlib.use("Agg")  # no GUI backend needed on a server
import matplotlib.pyplot as plt

from django.shortcuts import render

COINS = "bitcoin,ethereum,solana,dogecoin"
CURRENCY = "usd"
URL = (
    f"https://api.coingecko.com/api/v3/simple/price"
    f"?ids={COINS}&vs_currencies={CURRENCY}&include_market_cap=true"
)


def fetch_prices():
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
    coins = list(data.keys())
    market_caps = [data[coin][f"{CURRENCY}_market_cap"] for coin in coins]
    return coins, market_caps


def make_pie_chart(coins, market_caps):
    fig, ax = plt.subplots(figsize=(5, 5))
    def autopct_fmt(pct):
        return f"{pct:.1f}%" if pct >= 3 else ""

    wedges, _, _ = ax.pie(market_caps, autopct=autopct_fmt, pctdistance=0.75, startangle=90)
    ax.set_title("Market Cap Share")
    ax.legend(wedges, coins, title="Coin", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def index(request):
    chart_image = None
    fetched_at = None
    error = None

    if "fetch" in request.GET:
        try:
            coins, market_caps = fetch_prices()
            chart_image = make_pie_chart(coins, market_caps)
            fetched_at = datetime.now().strftime("%b %d, %Y %I:%M %p")
        except requests.exceptions.RequestException:
            error = "Couldn't fetch prices right now. Try again in a moment."

    return render(request, "charts/index.html", {
        "chart_image": chart_image,
        "error": error,
        "fetched_at": fetched_at,
    })