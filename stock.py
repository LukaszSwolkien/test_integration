#!./venv/bin/python
"""
Usage: 
    stock <symbol>
"""


from locale import currency
import logging
from docopt import docopt
import sys
from settings import conf
import signalfx
import yfinance as yf


def send_metrics(stock):
    def metric(name):
        return {
            "metric": name,
            "value": stock.get(name, 0),
            "dimensions": {
                "symbol": stock["symbol"],
                "currency": stock["currency"],
            },
        }

    with signalfx.SignalFx(ingest_endpoint=conf.SPLUNK_METRICS_INGEST).ingest(
        conf.SPLUNK_INGEST_TOKEN
    ) as sfx:
        sfx.send(
            gauges=[
                metric("price"),
                metric("volume"),
                metric("market_cap"),
                metric("total_cash"),
                metric("total_debt"),
                metric("total_revenue"),
                metric("target_mean_price"),
            ]
        )


def get_market_data(symbol):
    stock = yf.Ticker(symbol)
    return {
        "symbol": symbol,
        "currency": stock.info.get("currency", "USD"),
        "price": stock.info.get("regularMarketPrice", 0),  # currentPrice ?
        "volume": stock.info.get("volume", 0),
        "market_cap": stock.info.get("marketCap", 0),
        "total_cash": stock.info.get("totalCash", 0),
        "total_debt": stock.info.get("totalDebt", 0),
        "total_revenue": stock.info.get("totalRevenue", 0),
        "target_mean_price": stock.info.get("targetMeanPrice", 0),
    }


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    arguments = docopt(__doc__)
    symbol = arguments["<symbol>"]
    market_data = get_market_data(symbol)
    send_metrics(market_data)
