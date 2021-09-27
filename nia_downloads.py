import json
import os
from os import listdir
from os.path import isfile, join
import shutil
from time import sleep
import urllib.request
import sys

if (len(sys.argv) != 3):
	print('usage: nia_links.py <search string> <config filepath>')
	exit(1)
else:
	search = sys.argv[1]
	config = sys.argv[2]

def loadJson(filepath):
	f = ''
	with open(filepath, 'r') as file:
		f = json.load(file)
	return f

def sanitizeURL(url):
	finalURL = url.replace(' ', '%20')
	return finalURL

# Returns a list of existing filepaths in the specified directory
def getExistingFiles(directory):
	files = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
	fileset = set(files)	
	return files

def getImageURL(json):
	dlink = ''
	for link in json:
		if (link.find('~orig') > -1):
			dlink = sanitizeURL(link)
			break
	return dlink

# Read config file and set variables
jcnt = 1
jconfig = loadJson(config)
istart = jconfig['img_dir']
ijstart = jconfig['img_json_dir']
jstart = jconfig['page_json_dir'] + 'json_' + search
jfile = jstart + '_' + str(jcnt) + '.json'
loop = os.path.isfile(jfile)

print('nia_download gathering current file data...')
currentImages = getExistingFiles(istart)
print('Found ' + str(len(currentImages)) + ' files in image directory')
print('nia_download fetching...')
while loop:
	print('reading ' + jfile + '...')
	j = loadJson(jfile)
	itemData = j['collection']['items']
	for item in itemData:
		nasa_id = item['data'][0]['nasa_id']
		isubfile = istart + nasa_id
		ijfile = ijstart + nasa_id + '.json'
		if (ijfile in currentImages):
			print('image ' + nasa_id + ' already exists, skipping')
		else:
			print('downloading ' + nasa_id)
			ij = loadJson(ijfile)
			dlink = getImageURL(ij)
			sleep(1)
			try:
				with urllib.request.urlopen(dlink) as r:
					ext = r.info().get_content_subtype()
					ifile = isubfile + '.' + ext
					print('saving as ' + ifile)
					with open(ifile, 'wb') as out:
						shutil.copyfileobj(r, out)
			except urllib.error.HTTPError as http:
				print('\tHTTPError: ' + str(http))
				print('\tError nasa_id: ' + nasa_id)
				print('\tError URL: ' + dlink)
				pass
			except urllib.error.URLError as url:
				print('\tURLError: ' + str(url))
				print('\tError nasa_id: ' + nasa_id)
				print('\tError URL: ' + dlink)
				pass
			except http.client.InvalidURL as invalid:
				print('\tInvalidURL: ' + str(invalid))
				print('\tError nasa_id: ' + nasa_id)
				print('\tError URL: ' + dlink)
				pass
			except Exception as e:
				print('\tException: ' + str(e))
				print('\tError nasa_id: ' + nasa_id)
				print('\tError URL: ' + dlink)
			
	jcnt += 1
	jfile = jstart + '_' + str(jcnt) + '.json'
	loop = os.path.isfile(jfile)
