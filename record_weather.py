"""Record local weather data and forecasts
"""
import datetime
import json
import os

import requests

import config

# Query the Dark Sky API
# Use gzip encoding to minimize data transfer
url = '{base_url}/{api_key}/{home_lat},{home_lon}'.format(**config.dark_sky)
resp = requests.get(url, headers={'Accept-Encoding': 'gzip'})
resp.raise_for_status()

# Record the response.
# Each response gets its own JSON file (~27 kB)
# Rotate directories every month
now = datetime.datetime.now()
weather_dir = os.path.join(config.data_dir, now.strftime('%Y%m'))
weather_fname = now.strftime('%Y%m%d_%H%M%S.json')
os.makedirs(weather_dir, exist_ok=True)
with open(os.path.join(weather_dir, weather_fname), 'wt') as _fout:
    json.dump(resp.json(), _fout)
