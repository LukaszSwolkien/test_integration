#!./venv/bin/python
"""
Usage: 
    market_cap <coin_id>
"""


import logging
from docopt import docopt
import sys
from settings import conf
import signalfx
from pycoingecko import CoinGeckoAPI


def send_metrics(coin_stats):
    def metric(name):
        return {
            "metric": name,
            "value": coin_stats.get(name, 0),
            "dimensions": {
                "crypto_id": coin_stats["id"],
                "currency": coin_stats["currency"],
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
                metric("market_cap_rank"),
            ]
        )


def get_market_data(id, currency="usd"):
    def get_coin_value(coin, parameter, currency, default=0):
        return coin.get("market_data", {}).get(parameter, {}).get(currency, default)

    cg = CoinGeckoAPI()
    coin = cg.get_coin_by_id(id)

    market_data = coin.get("market_data")
    current_price = get_coin_value(coin, "current_price", currency)
    market_cap = get_coin_value(coin, "market_cap", currency)
    volume = get_coin_value(coin, "total_volume", currency)
    market_cap_rank = market_data.get("market_cap_rank", 0)

    coin_data = {
        "id": id,
        "currency": currency,
        "price": current_price,
        "market_cap": market_cap,
        "volume": volume,
    }

    if market_cap_rank is not None:
        coin_data["market_cap_rank"] = market_cap_rank

    return coin_data


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    arguments = docopt(__doc__)
    coin_id = arguments["<coin_id>"]
    market_data = get_market_data(coin_id)
    send_metrics(market_data)
