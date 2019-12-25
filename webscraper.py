from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'http://www.fyan8.com/yueyu2/xt3.htm'
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser", from_encoding="gb18030")
containers = page_soup.find_all("td", "nrct")
plaintext = containers[0]
plaintext = str(plaintext).replace("<br/>","").replace("\n", "").replace("</td>","")
aindex = plaintext.find("</a>") + 4
plaintext = plaintext[aindex:]
print(plaintext)