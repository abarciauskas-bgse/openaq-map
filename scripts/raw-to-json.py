import csv
import json
import pandas as pd
import numpy as np
from datetime import date, timedelta
import urllib2

start_date = date(2018, 1, 1)
end_date = date(2018, 3, 23)
base_url = 'https://openaq-data.s3.amazonaws.com/'
current_date = start_date

while current_date < end_date:
  current_date_string = current_date.strftime('%Y-%m-%d')
  contents = csv.DictReader(urllib2.urlopen(base_url + current_date_string + '.csv'))
  raw_observations = list(contents)

  metric = 'pm25'
  df = pd.DataFrame(raw_observations)
  df_pms = df[df['parameter'] == metric]
  groups = df_pms.groupby('location')

  averages = []
  for name, group in groups:
    average_for_location = {}
    average_for_location['location'] = name
    average_for_location['average'] = np.mean(group['value'].astype(np.float))
    first_item = group.head(1)
    average_for_location['city'] = first_item['city'].iloc[0] # safe assumption
    try:
      average_for_location['latitude'] = np.float(first_item['latitude'])
      average_for_location['longitude'] = np.float(first_item['longitude'])
      averages.append(average_for_location)
    except:
      print "Can't convert lat / lon for " + name + "."

  with open('../data/generated/' + current_date_string + '.json', 'w') as outfile:
      json.dump(averages, outfile, indent=2, sort_keys=False, ensure_ascii=False)

  print('Done with ' + current_date_string)
  current_date = current_date + timedelta(days=1)

