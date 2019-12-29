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

	

def num_there(s):
	return any(i.isdigit() for i in s)

def sentence_eraser(plaintext):
	sentence_with_number_index = []
	numberExists = False
	plaintextlist = plaintext.replace('\n','').split('。')
	plaintext = ''
	for i in range(len(plaintextlist)):
		if num_there(plaintextlist[i]):
			sentence_with_number_index.append(i)
	number = 0
	for i in sentence_with_number_index:
		plaintextlist.pop(i - number)
		number = number + 1
	for i in plaintextlist:
		if len(i) > 0:
			plaintext = plaintext + i + '。'
	return plaintext
# coding=gbk
def wiki_dataset_cleaner(plaintext):
    for i in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏！？｡aeiouvüāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜAEIOUVÜĀĒĪŌŪǕÁÉÍÓÚǗǍĚǏǑǓǙÀÈÌÒÙǛ"#$%&\'()*+,-/:;<=>@[]^_`{|}~".!?ê█■':
        if i == '。':
            plaintext = plaintext.replace(i,"。\n")
        elif i == '^':
            plaintext = plaintext.replace("^。","！\n")
        elif i == '*':
            plaintext = plaintext.replace("*。","？\n")
        else:
            plaintext = plaintext.replace(i, "")

    return plaintext.replace(" ", "")   

    """ 
    for some reason 顏色指引????????劇集????????
    綜藝脫口騷節目????????紀錄片專題片????????選騷音樂節目????????
    真人騷節目????????文化社科節目????????生活服務節目註標嘅節目湖南衛視擁有完整版權。
    註標的節目湖南衛視擁有完整版權。以下劇目喺網絡平台全部由芒果全網獨播。 
    does not get filtered

    additional symbols not accounted for:
    ∈\\^∈\\^τ∈\\\\×\\^\\ and occasionally japanese
    '?' keep appearing

    """

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
	if plaintext != '':
		plaintext = wiki_dataset_cleaner(sentence_eraser(plaintext).replace("！","^。").replace("？","*。"))

	return plaintext

openFile = open("url_list.txt","r")
dataFile = open("training_data.txt","w",encoding="gb18030")
my_url_list = openFile.read().split()

for url in my_url_list:
	my_url = url
	dataFile.write(parser(my_url) + '\n')

openFile.close()
dataFile.close()
