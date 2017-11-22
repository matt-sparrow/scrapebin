import sched
import time
import certifi
import urllib3
import json
import re
import os
from threading import Timer

## Global key buffer
bufKeys = []

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


def scrapeKeys():
	## Pull 100 most recent keys from pastebin
	## Pass it to pulseKeys for storage
	url = 'https://pastebin.com/api_scraping.php?limit=100'
	global bufKeys
	keys = []

	## Request data from pastebin
	http = urllib3.PoolManager(
		cert_reqs = 'CERT_REQUIRED',
		ca_certs = certifi.where())
	req = http.request('GET', url)
	r = req.data
	content = json.loads(r.decode('utf-8'))

	for item in content:
		if item['key'] in bufKeys:
			## print('Key is in key buffer')
			pass
		else:
			bufKeys.append(item['key'])
			bufKeys = bufKeys[-200:]
			pulseKeys(1, item['key'])

	return 1

def scrapeContent():
	key = pulseKeys(0, 0)

	if key == None:
		## print('No key to scrape, waiting...')
		return

	url = 'https://pastebin.com/api_scrape_item.php?i='
	email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b")

	http = urllib3.PoolManager(
		cert_reqs = 'CERT_REQUIRED',
		ca_certs = certifi.where())
	req = http.request('GET', url + key.rstrip())
	r = req.data
	content = r.decode('utf-8')
	if email_regex.match(content):
		results = email_regex.findall(content)
		if len(results) >= 10:
			print('Total e-mails found in ' + str.rstrip(key) + ': ' + str(len(results)))
##
			file = open(str.rstrip(key) + ".txt", "a+")
			for email in results:
				file.write(email + '\n')
##
		else:
			pass
	else:
		pass

	return 1


def pulseKeys(bStore, key):
	## Arguments: bStore 0/1
	keyfile = 'pastebin.keys'
	keys = []

	if bStore == 0:
		## Pull a key
		if os.stat(keyfile).st_size == 0:
			## print('Empty file, waiting for keys.')
			return None

		else:
			with open(keyfile, 'r') as fin:
				keys = fin.read().splitlines(True)
			with open(keyfile, 'w') as fout:
				fout.writelines(keys[1:])

			keys[0].replace('\n', '')
			return keys[0]

	elif bStore == 1:
		## Store a key

		## Check to see if it's a duplicate
		with open(keyfile) as f:
			for curKey in f:
				keys.append(curKey)

		file = open(keyfile, "a+")

		if (key + '\n') in keys:
			## print('Duplicate key, not saved.\n')
			return 0

		else:
			file.write(key + '\n')
			## print('Unique key, saved.\n')
			return 1

if not os.path.isdir("./pastes"):
	os.makedirs("./pastes")
if not os.path.isfile("./pastebin.keys"):
	open("./pastebin.keys", "a")

t1 = RepeatedTimer(1.75, scrapeContent)
t2 = RepeatedTimer(90, scrapeKeys)


