"""Query my Rainforest EAGLE and record the response
"""
import csv
import datetime
import os

import RainEagle

import config

raineagle = RainEagle.Eagle(debug=False, checkfirmware=False, **config.eagle)

columns = ['demand_timestamp', 'demand', 'demand_units', 
           'summation_delivered', 'summation_units', 
           'price', 'price_units']

# Initialize output file if it doesn't exist
# Rotate files every day
date = datetime.datetime.now().strftime('%Y%m%d')
base_fname = '{}_electricity.csv'.format(date)
full_fname = os.path.join(config.data_dir, base_fname)

os.makedirs(os.path.dirname(full_fname), exist_ok=True)
if not os.path.exists(base_fname):
    with open(full_fname, 'w') as _fout:
        _fout.write(','.join(columns))
        _fout.write('\n')

# Fetch and write current electricity usage data
with open(full_fname, 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, delimiter=',', 
                            extrasaction='ignore',
                            fieldnames=columns,
                            quotechar='"', 
                            quoting=csv.QUOTE_MINIMAL)
    usage_data = raineagle.get_usage_data()
    writer.writerow(usage_data)
