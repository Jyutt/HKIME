from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import urllib.request

my_url = 'https://lihkg.com/thread/1797/page/1'

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0"
opener = AppURLopener()
page_html = opener.open(my_url).read()
page_soup = soup(page_html, "html.parser", from_encoding="gb18030")

def fyan8_parser():
    for i in page_soup.select(".nrct"):
        print (i.get_text().strip())
def wikipedia_parser():
    for i in page_soup.select('p'):
        print(i.get_text().strip())
def lihkg_parser():
    containers = page_soup.find_all("div", class_ = "_3jxQCFWg9LDtkSkIVLzQ8L")
    print(containers)
    for i in page_soup.select("div._2cNsJna0_hV8tdMj3X6_gJ"):
        print(i.get_text().strip())
#lihkg parser does not work
