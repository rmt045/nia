import sys
import subprocess

if(len(sys.argv) != 3):
	print('usage: main.py <search string> <config filepath>')
	exit(1)
else:
	search = sys.argv[1]
	config = sys.argv[2]
	print('NASA Image API Crawl for search: ' + search)
	print('Configuration file: ' + config)
	print('Running JSON Fetcher')
	cmd = ['python3', 'nia_json.py', search, config]
	subprocess.Popen(cmd).wait()
	print('Running Link Fetcher')
	cmd = ['python3', 'nia_links.py', search, config]
	subprocess.Popen(cmd).wait()
	print('Running Downloader')
	cmd = ['python3', 'nia_downloads.py', search, config]
	subprocess.Popen(cmd).wait()
	print('Gathering Updated Terms')
	cmd = ['python3', 'nia_terms.py', config]
	subprocess.Popen(cmd).wait()
	print('DONE')
