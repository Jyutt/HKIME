from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://zh-yue.wikipedia.org/wiki/%E7%B2%B5%E6%96%87%E7%B6%AD%E5%9F%BA%E7%99%BE%E7%A7%91'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser", from_encoding="gb18030")

def fyan8_parser():
    for i in page_soup.select(".nrct"):
        print (i.get_text().strip())
def wikipedia_parser():
    for i in page_soup.select('p'):
        print(i.get_text().strip())

if "wikipedia" in my_url:
    wikipedia_parser()
if "fyan" in my_url:
    fyan8_parser()
