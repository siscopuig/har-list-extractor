 # Captures all ajax requests are done by an URL using a proxy server, then stores
 # all links requested in a text file for further processing.

# Still in development!!

from browsermobproxy import Server
from selenium import webdriver
import json
import datetime
import time
import re


def run_servers(url, har_export_path, headless=None):

	server = Server("../browsermob-proxy-2.1.4/bin/browsermob-proxy")
	server.start()
	proxy = server.create_proxy()

	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
	chrome_options.add_argument('--window-size=1366,768')

	if headless:
		chrome_options.add_argument('--headless')

	driver = webdriver.Chrome(chrome_options = chrome_options)


	# From url, extract parameter for new_har function. It's a reference.
	new_har_ref = get_domain(url)

	proxy.new_har(new_har_ref)
	driver.get(url)
	time.sleep(6)

	with open(har_export_path, 'w') as outfile:
		json.dump(proxy.har, outfile)

	server.stop()
	driver.quit()


def read_from_file(path):

	with open(path, 'r') as file:
		return file.readlines()


def append_to_file(urls, list_path):

	with open(list_path, 'a') as file:
		for url in urls:
			file.write('\n' + url)


def get_urls_from_string(data):

	string = str(data)
	urls = re.findall('http[s]?://(?:(?!http[s]?://)[a-zA-Z]|[0-9]'
					  '|[$\-_@.&+/]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
	if not urls:
		return None
	return urls


def get_domain(url):

	source = re.compile(r"https?://(www\.)?")
	src =  source.sub('', url)
	return src.split('/')[0]




page = '<insert your url here>'

domain = get_domain(page)
datetime_path = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
filename = '{domain}_{datetime_path}'.format(domain=domain, datetime_path=datetime_path)


har_path = 'har/{filename}.txt'.format(filename=filename)
output_path = 'output/{filename}.txt'.format(filename=filename)

# Run page and create the HAR file
run_servers(page, har_path)

# Read HAR file, process links and append links to a file line by line
har_file = read_from_file(har_path)
links = get_urls_from_string(har_file)
append_to_file(links, output_path)


# Print links
for link in links:
	print(link)








