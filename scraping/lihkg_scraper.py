from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time

# set URL
driver = webdriver.Firefox()
driver.get(url)


# Manually scroll
time.sleep(100)

res = driver.execute_script("return document.documentElement.outerHTML")
page_soup = soup(res, 'lxml')
str_res = str(res)

# pagesource = driver.page_source
# page_soup = soup(pagesource, 'lxml')

for i in page_soup.select('._2cNsJna0_hV8tdMj3X6_gJ'):
    print(i)
