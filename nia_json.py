import json
import os
import requests
from time import sleep
import sys

if (len(sys.argv) != 3):
	print('usage: nia_json.py <search string> <config filepath>')
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
running = 0
jconfig = loadJson(config)
urlBase = jconfig['base_url']
jfile = jconfig['page_json_dir'] + 'json_'
url = urlBase + search

print('nia_json crawling with search: ' + search + '...')
while url:
	print('current url: ' + url)
	try:
		sleep(1)
		r = requests.get(url)
		httpCode = r.status_code
		r.raise_for_status()
		j = r.json()
		count = len(j['collection']['items'])
		running = running + count
		total = j['collection']['metadata']['total_hits']
		print(str(httpCode) + ' ' + url)
		print('total=' + str(total) + ' running=' + str(running) + ' count=' + str(count))
		print('downloading json...')
		with open(jfile + search + '_' + str(jcnt) + '.json', 'w') as f:
			json.dump(j, f)
		jcnt += 1
		next = ''
		if 'links' in j['collection']:
			for link in j['collection']['links']:
				if link['rel'] == 'next':
					next = link['href']
					print('next url: ' + next)
		url = next
			
	except requests.exceptions.HTTPError as http:
		code = http.response.status_code
		print('HTTP Error ' + str(code))
		if (code == 400):
			print('Bad request')
		elif (code == 404):
			print('Results not found')
			print(j)
		elif (code >= 500):
			print('Server error')
		break
	except requests.exceptions.ConnectionError as conn:
		print('ConnectionError ' + str(conn))
	except requests.exceptions.Timeout as time:
		print('Timeout ' + str(time))
	except Exception as e:
		print('Exception: ' + str(e))
print('done')
