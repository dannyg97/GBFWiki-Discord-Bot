import requests
import re
from bs4 import BeautifulSoup


def init(search: str):
	request_url = "https://gbf.wiki/index.php?search=" + search + "&title=Special%3ASearch&go=Go"
	page = requests.get(request_url)
	return [BeautifulSoup(page.text, "html.parser"), page.url]


search_query = init(input("Who do you want to search up?"))
soup, url = search_query[0], search_query[1]
print(f"Page URL: {url}")
print(f"Gameplay notes: {url}#Gameplay_Notes")

for span in soup.findAll("span", class_="tooltiptext"):
	span.decompose()

result = soup.findAll("table", class_='wikitable')
traits = ""
mydivs = result[0].find("div", {"class": "char-name"})
print(mydivs.text)

# Finds traits
for cell in result[1].find_all('a', href=True):
	category_res = re.search('(?<=:).*(?=_)', cell['href'])
	if category_res:
		res = category_res.group(0)
		if len(res) < 10:
			if traits == "":
				traits += res
			else:
				traits += ", " + res

print(f"Traits: {traits}")

# Finds description
for cell in result[5].find_all('td'):
	print(f"Description: {cell.text}")

# Finds, formats charge attack
ca_counter = 0
for cell in result[6].find_all('td'):
	if ca_counter not in [0, 3]:
		if ca_counter % 3 == 1:
			to_string = str(cell.text)
			to_string = re.sub("After 5★", "", to_string)
			print(f"Charge attack: {to_string}")
		else:
			print(f"{cell.text}")
	ca_counter += 1

# Finds, formats skill details
skill_counter = 0
for cell in result[7].find_all('td'):
	to_print = str(cell.text)
	to_print = re.sub(r"\[[0-9]\]", "", to_print)
	if "enhanced at level" in str(cell.text):   #not that important
		to_print = re.sub(r"This skill is enhanced at level \d\d.", " ", to_print)
		to_print = re.sub(r"This skill is enhanced again at level \d\d.", " ", to_print)
		to_print = re.sub(r"Complete a Fate Episode to unlock.", " ", to_print)
		print(f"{to_print}")
	elif str(cell.text) == "  ":
		continue
	elif skill_counter % 5 == 0:
		print(f"Skill: {to_print}")
	# elif skill_counter in [3, 6,]:
	# 	pass
	else:
		print(f"{to_print}")

	skill_counter += 1


# finding what table contains what
# for i in range(len(result)):
# 	print(f"======================= UP TO {i}")
# 	print(result[i])

"""
For image/art scraping 

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

# To get description
for cell in result[5].find_all('td'):
	print(cell.text)
	
result[6] contains charge attack
"""