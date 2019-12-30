from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import urllib.request


class AppURLopener(urllib.request.FancyURLopener):
	version = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"

opener = AppURLopener()

def wiki_quotes_eraser(plaintext, amount):
	for i in range(1,amount+1):
		quotes = "[" + str(i) + "]"
		plaintext = plaintext.replace(quotes,"")
	return plaintext

def parser(my_url):
	plaintext = ''
	page_html = opener.open(my_url).read()
	page_soup = soup(page_html, "html.parser", from_encoding="gb18030")
	amount_of_quotes = len(page_soup.find_all("span", "mw-cite-backlink"))
	if "wikipedia" or "appledaily" in my_url:
		for i in page_soup.select('p'):
			plaintext = wiki_quotes_eraser(i.get_text().strip(),amount_of_quotes) + plaintext
	elif "fyan" in my_url:
		for i in page_soup.select(".nrct"):
			plaintext = i.get_text().strip() + plaintext

	return plaintext

openFile = open("url_list.txt","r")
dataFile = open("raw_training_data.txt","w",encoding="gb18030")
my_url_list = openFile.read().split()

for url in my_url_list:
	my_url = url
	dataFile.write(parser(my_url) + '\n')

openFile.close()
dataFile.close()
