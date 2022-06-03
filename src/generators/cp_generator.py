# pylint: disable=import-error
# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
""" Champion Point crawler """ 
import json
import requests
from bs4 import BeautifulSoup as bs

# BASE_URL = 'https://esoitem.uesp.net/viewCps.php?version=33'
BASE_URL = "https://esoitem.uesp.net/viewlog.php?record=cp2Skills29pts"

raw_page = requests.get(BASE_URL)
soup = bs(raw_page.content, 'lxml')

table = soup.find_all('tr')
titles_of_table = []
ids = set()
skills = [
    {'disciplineId': {'Craft': 1, 'Warfare': 2, 'Fitness': 3}, 'serverPatch': 29}
]

for index_of_table, content in enumerate(table):
    if index_of_table != 0:
        # Tenemos que saltar la primera fila porque contiene el "View" y no es util
        champion_skill = {}
        for index, row in enumerate(content.find_all('td')[1:]):
            if row.text != '':
                champion_skill[titles_of_table[index]] = row.text
        skills.append(champion_skill)
    else:
        for row in content.find_all('th'):
            if row.text != "":
                titles_of_table.append(row.text)

with open("src/champion_points/cp.json", 'w+', encoding='utf-8') as file:
    json.dump(skills, file, indent=4)
