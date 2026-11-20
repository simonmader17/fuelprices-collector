import requests
from datetime import datetime, timedelta
import psycopg2
import time
import logging
import os
import sys
logging.basicConfig(
    format='%(asctime)s [ %(levelname)-8s ] %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)


DATABASE_URL = os.environ.get("DATABASE_URL", "db:5432")
DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "fuelprices")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "fuelprices")


def write_fuel_prices(timestamp, jet, avanti, jet_langenrohr, bp):
    host, _, port = DATABASE_URL.partition(":")
    connection = None
    try:
        connection = psycopg2.connect(user=DATABASE_USERNAME,
                                      password=DATABASE_PASSWORD,
                                      host=host,
                                      port=port or "5432",
                                      database="fuelprices")
        cursor = connection.cursor()
        insert_query = """insert into fuelprices (timestamp, jet, avanti, jet_langenrohr, bp) values (%s, %s, %s, %s, %s)"""
        insert_values = (timestamp, jet, avanti, jet_langenrohr, bp)
        cursor.execute(insert_query, insert_values)
        logging.info("Inserted: (%s, %s, %s, %s, %s)" % insert_values)
        connection.commit()
    except Exception as error:
        logging.error("Error while writing to PostgreSQL: %s", error)
    finally:
        if connection:
            connection.close()


def get_price_of_gas_station(params, id):
    url = "https://api.e-control.at/sprit/1.0/search/gas-stations/by-address"
    res = requests.get(url=url, params=params)
    data = res.json()
    result = next((item for item in data if item["id"] == id), None)
    price = next((price for price in result["prices"]), None)
    if price is None:
        return None
    return price["amount"]


def fuel_prices():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S+02")

    # Avanti St. Pölten
    params = dict(
        latitude=48.2067799743733,
        longitude=15.64137878463607,
        fuelType="SUP",
        includeClosed="false"
    )
    price_avanti = get_price_of_gas_station(params, 1354797)

    time.sleep(2)

    # Jet St. Pölten
    params = dict(
        latitude=48.18980282362078,
        longitude=15.61827453516601,
        fuelType="SUP",
        includeClosed="false"
    )
    price_jet = get_price_of_gas_station(params, 1354952)

    time.sleep(2)

    # Jet Langenrohr
    params = dict(
        latitude=48.3186840860446,
        longitude=16.0212912048759,
        fuelType="SUP",
        includeClosed="false"
    )
    price_jet_langenrohr = get_price_of_gas_station(params, 1354956)

    time.sleep(2)

    # BP Böheimkirchen
    params = dict(
        latitude=48.19106866623074,
        longitude=15.766024098126344,
        fuelType="SUP",
        includeClosed="false"
    )
    price_bp = get_price_of_gas_station(params, 35664)

    if price_jet is not None or price_avanti is not None or price_jet_langenrohr is not None or price_bp is not None:
        write_fuel_prices(timestamp, price_jet, price_avanti, price_jet_langenrohr, price_bp)


def seconds_until_next_run(now=None):
    """Seconds until the next :00:10 or :30:10 (10 s after the full/half hour)."""
    now = now or datetime.now()
    slot = now.replace(minute=0 if now.minute < 30 else 30, second=10, microsecond=0)
    if slot <= now:
        slot += timedelta(minutes=30)
    return (slot - now).total_seconds()


if __name__ == "__main__":
    if "--once" in sys.argv or os.getenv("RUN_ONCE") == "1":
        fuel_prices()
        sys.exit(0)

    logging.info("Starting collector, collecting at :00 and :30")
    while True:
        time.sleep(seconds_until_next_run())
        try:
            fuel_prices()
        except Exception:
            logging.exception("Collecting fuel prices failed")
