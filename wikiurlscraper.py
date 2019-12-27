import requests
import urllib

def get_response(url):
	S = requests.Session()
	R = S.get(url=url)
	return R.json()

nextWiki = '%21'
dataFile = open("url_list.txt","w",encoding="gb18030")
dataFile.close
while nextWiki != '':
	apfromstr = '&apfrom=' + nextWiki
	url = 'https://zh-yue.wikipedia.org/w/api.php?action=query&list=allpages&format=json&aplimit=500' + apfromstr

	DATA = get_response(url)
	PAGES = DATA["query"]["allpages"]
	NEXTWIKI = DATA["continue"]["apcontinue"]

	dataFile = open("url_list.txt","a",encoding="gb18030")
	for page in PAGES:
		wikiUrl = 'https://zh-yue.wikipedia.org/wiki/'
		wikiUrl = wikiUrl + page["title"]
		url = urllib.parse.quote(wikiUrl.encode('utf8'), ':/')
		dataFile.write(url + '\n')
	nextWiki = NEXTWIKI	


dataFile.close()