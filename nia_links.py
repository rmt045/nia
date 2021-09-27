import json
import os
import requests
import shutil
import urllib.request
from time import sleep
import sys

if (len(sys.argv) != 3):
	print('usage: nia_links.py <search string> <config filepath>')
	exit(1)
else:
	search = sys.argv[1]
	config = sys.argv[2]

def loadJson(filepath):
	f = ''
	with open(filepath, 'r') as cfile:
		f = json.load(cfile)
	return f

# Read config file and set variables
jcnt = 1
data = []
jconfig = loadJson(config)
idir = jconfig['img_dir']
jdir = jconfig['page_json_dir']
ijdir = jconfig['img_json_dir']
jfile = jdir + 'json_' + search + '_' + str(jcnt) + '.json'
loop = os.path.isfile(jfile)

print('nia_links crawling...')
while loop:
	print('reading ' + jfile + '...')
	with open(jfile, 'r') as f:
		j = json.load(f)
		itemData = j['collection']['items']
		for item in itemData:
			jlink = item['href']
			nasa_id = item['data'][0]['nasa_id']
			ijfile = ijdir + nasa_id + '.json'
			if (os.path.isfile(ijfile) == False):
				try:
					sleep(1)
					print('fetching ' + nasa_id)
					jr = requests.get(jlink)
					jr.raise_for_status()
					jrCode = jr.status_code
					ij = jr.json()
					with open(ijfile, 'w') as f:
						json.dump(ij, f)
				except requests.exceptions.HTTPError as http:
					code = http.response.status_code
					print('HTTP Error ' + str(code))
					if (code == 400):
						print('Bad request')
					elif (code == 404):
						print('Results not found')
					elif (code >= 500):
						print('Server error')
					print(str(http))
				except requests.exceptions.ConnectionError as conn:
					print('ConnectionError ' + str(conn))
				except requests.exceptions.Timeout as time:
					print('Timeout ' + str(time))
				except Exception as e:
					print('Exception: ' + str(e))
			else:
				print('skipping ' + nasa_id)
	jcnt += 1
	jfile =jdir + 'json_' + search + '_' + str(jcnt) + '.json'
	loop = os.path.isfile(jfile)
print('done')
