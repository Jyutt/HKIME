from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time

# set URL
url = "https://lihkg.com/thread/1849750"
driver = webdriver.Firefox()
driver.get(url)


SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

for i in range(10):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    # if new_height == last_height:
    #     break
    # last_height = new_height
    print(f"Finished scrolling iteration {i}, last height: {last_height}")


res = driver.execute_script("return document.documentElement.outerHTML")
page_soup = soup(res, 'lxml')
str_res = str(res) 

for i in page_soup.select('._2cNsJna0_hV8tdMj3X6_gJ'):
    print(i)