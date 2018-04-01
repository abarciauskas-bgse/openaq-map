from os import listdir
from os.path import isfile, join
import json

directory = 'data/generated/'
onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]

day_averages_by_location = {}

for file in onlyfiles:
  data = json.loads(open(directory + file).read())
  

