import requests
import re
from bs4 import BeautifulSoup

session = requests.Session()
api = "https://gbf.wiki/api.php"
request = "Medusa"  # Change this to be input later

parameters = {
	'action': "parse",
	'page': request,
	'format': "json"
}

result = session.get(url=api, params=parameters)
soup = BeautifulSoup(result.content, 'lxml')

image = soup.find_all(attrs={'srcset':True})
regex = re.compile(r".png'")
linkToImage = ""
for i in image:
	if bool(re.search('01\.png', i['srcset'])):
		linkToImage = i['srcset']
		linkToImage = linkToImage[2:]
		linkToImage = "gbf.wiki" + linkToImage
		print(linkToImage)
		break
