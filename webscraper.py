from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import urllib.request


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"


opener = AppURLopener()


def parser(my_url):
    plaintext = ''
    page_html = opener.open(my_url).read()
    page_soup = soup(page_html, "html.parser", from_encoding="gb18030")
    if "wikipedia" in my_url:
        for i in page_soup.select('p'):
            plaintext = i.get_text().strip() + plaintext
    else:
        for i in page_soup.select(".nrct"):
            plaintext = i.get_text().strip() + plaintext
    return plaintext


openFile = open("url_list.txt", "r") #reads a list of urls to scrape
dataFile = open("traning_data.txt", "x") #creates a file to store data from url
dataFile.close()
dataFile = open("traning_data.txt", "a")
my_url_list = openFile.read().split()
for url in my_url_list:
    my_url = url
    dataFile.write(parser(my_url) + '\n\n')
    
openFile.close()
dataFile.close()

