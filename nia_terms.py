import json
from contextlib import redirect_stdout
from os import listdir
from os.path import isfile, join
import sys

def loadJson(filepath):
	f = ''
	with open(filepath, 'r') as file:
		f = json.load(file)
	return f

# Read config file and set variables
config = sys.argv[1]
centers = set()
keywords = set()
locations = set()
photographers = set()
secondaryCreators = set()
albums = set()
jconfig = loadJson(config)
jdir = jconfig['page_json_dir']
output = jconfig['terms_filepath']
files = [join(jdir, f) for f in listdir(jdir) if isfile(join(jdir, f))]

for f in files:
	j = loadJson(f)
	itemData = j['collection']['items']
	for item in itemData:
		data = item['data'][0]
		try:
			centers.add(data['center'])
		except:
			pass
		try:
			for keyword in data['keywords']:
				keywords.add(keyword)
		except:
			pass
		try:
			locations.add(data['location'])
		except:
			pass
		try:
			photographers.add(data['photographer'])
		except:
			pass
		try:
			secondaryCreators.add(data['secondary_creator'])
		except:
			pass
		try:
			for album in data['album']:
				albums.add(album)
		except:
			pass

with open(output, 'w') as o:
	with redirect_stdout(o):
		print('\t\t-----Centers-----')
		for center in sorted(centers):
			print(center)
		print('\t\t-----Locations-----')
		for location in sorted(locations):
			print(location)
		print('\t\t-----Keywords-----')
		for keyword in sorted(keywords):
			print(keyword)
		print('\t\t-----Photographers-----')
		for photographer in sorted(photographers):
			print(photographer)
		print('\t\t----Secondary Creators-----')
		for secondary in sorted(secondaryCreators):
			print(secondary)
		print('\t\t-----Albums-----')
		for album in sorted(albums):
			print(album)
