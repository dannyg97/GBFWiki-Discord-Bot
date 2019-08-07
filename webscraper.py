import requests
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
links = soup.find_all('a')
links2 = soup.find_all('a')
print(links2)
for link in links:
	if "Medusa" in link.text:
		print(link)
		print(link.attrs['title'])
