""" Skill generator """

import re
import json
import requests
from bs4 import BeautifulSoup as bs

raw_page = requests.get('https://esoitem.uesp.net/viewSkills.php')
soup = bs(raw_page.content, 'lxml')

base_skill_url = 'https://esoitem.uesp.net/viewlog.php?action=view&record=minedSkills&id='

skills = soup.find_all("div", {"class": "esovsAbilityBlockHover"})
i = 0

for skill in skills:
    url = base_skill_url + skill.get('skillid')
    skill_web_page = requests.get(url)
    table = bs(skill_web_page.content, 'lxml').find_all('tr')
    skill_dict = {}
    for i in table:
        table_id = i.find('th').text
        value = i.find('td').text
        if table_id == "texture":
            img_link = i.find('a').get('href')
            value = f'https:{img_link}'
        skill_dict[table_id] = value
    file_name = 'src/skills/'+skill_dict['name']+'.json'
    with open(file_name.replace(' ', '_'), 'w+', encoding='utf-8') as f:
        json.dump(skill_dict, f)
