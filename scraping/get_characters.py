# get a list of characters from dictionary to match frequency

import requests
from bs4 import BeautifulSoup
import math
from time import sleep
total_levels = 4
page = 0
count = 0
dataFile = open("char_list.txt", "w", encoding="utf-8")
for level in range(1, total_levels+1):
    URL = "http://www.cantonese.sheik.co.uk/scripts/masterlist.htm?action=onelevel&level=" + \
        str(level)+"&page="+str(page)
    # page is 0 indexed
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
    h4 = soup.find('h4')
    total_chars = int(h4.text.split()[3])
    total_pages = math.ceil(total_chars/50)
    for page in range(total_pages):
        URL = "http://www.cantonese.sheik.co.uk/scripts/masterlist.htm?action=onelevel&level=" + \
            str(level)+"&page="+str(page)
        # page is 0 indexed
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
        table = soup.find_all('a', attrs={'class': 'black'})
        for char in table:
            dataFile = open("char_list.txt", "a", encoding="utf-8")
            dataFile.write(char.text[0] + '\n')
            count += 1
        print("level " + str(level) + " page " + str(page))
        page += 1
        sleep(2)
    print(str(count)+" words in level " + str(level))
    count = 0
    page = 0

dataFile.close()
