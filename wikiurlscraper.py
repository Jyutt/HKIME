import requests
import urllib

def get_response(url):
	S = requests.Session()
	R = S.get(url=url)
	return R.json()

nextWiki = ''
breakLoop = False

dataFile = open("url_list.txt","w",encoding="gb18030")

while True:
	apfromstr = '&apfrom=' + nextWiki
	url = 'https://zh-yue.wikipedia.org/w/api.php?action=query&list=allpages&format=json&apminsize=10000&aplimit=500' + apfromstr

	DATA = get_response(url)
	PAGES = DATA["query"]["allpages"]
	if DATA.get("continue") != None:
		NEXTWIKI = DATA.get("continue")["apcontinue"]
	else:
		breakLoop = True
		nextWiki = ''
	dataFile = open("url_list.txt","a",encoding="gb18030")
	for page in PAGES:
		wikiUrl = 'https://zh-yue.wikipedia.org/wiki/'
		wikiUrl = wikiUrl + page["title"]
		url = urllib.parse.quote(wikiUrl.encode('utf8'), ':/')
		dataFile.write(url + '\n')
		nextWiki = NEXTWIKI	
	if breakLoop:
		break
	

dataFile.close()
