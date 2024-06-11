"""
A python service to emulate a timed LRU cache sending location of the vehicles.
"""

import datetime
import os

import requests
from flask import Flask

from timed_lru_cache import TimedLRUCache

ENDPOINT_TEMPLATE = os.environ.get("ENDPOINT_TEMPLATE", "https://postman-echo.com/get?vehicleID={}")
# alternate EP - "http://127.0.0.1:{}/get_location"
LRU_TIME_LIMIT = os.environ.get("LRU_TIME_LIMIT", 60)
LRU_TIME_LIMIT = datetime.timedelta(seconds=LRU_TIME_LIMIT)
LRU_SIZE_LIMIT = os.environ.get("LRU_SIZE_LIMIT", 16)
DEBUG = (os.environ.get("DEBUG", "False") == "True")

cache = TimedLRUCache(cache_size=LRU_SIZE_LIMIT, time_limit=LRU_TIME_LIMIT)
app = Flask(__name__)


@app.route('/')
def info():
    return "A python service to emulate a timed LRU cache."


@app.route('/get_location/<int:vehicleID>', methods=['GET'])
def get_location(vehicleID=None):
    """
    A function that uses an LRU cache to retrieve the location of a vehicle.
    :param vehicleID: ID of the vehicle whose location needs to be retrieved.
    :return: JSON List with [latitude, longitude]
    """

    global cache
    if not vehicleID:
        return "No ID specified", 404
    cache_hit = cache[vehicleID]

    if cache_hit:
        if DEBUG:
            print("cache hit")
        return cache_hit
    else:
        if DEBUG:
            print("fetching")
        response = requests.get(url=ENDPOINT_TEMPLATE.format(vehicleID))
        cache[vehicleID] = response.json()
        if DEBUG:
            print(len(cache.cache))
        return response.json()


if __name__ == '__main__':
    PORT = os.environ.get("PORT", 9090)
    app.run(host='0.0.0.0', port=PORT)
