""" Buff/Debuff generator"""

import re
import json
import requests
from bs4 import BeautifulSoup as bs


raw_page = requests.get('https://eso-u.com/articles/buffs_and_debuffs_the_majorminor_system')
soup = bs(raw_page.content, 'lxml')

tables = soup.find_all("table")
buff = True
for table in tables[2:]:
    rows = table.find_all("tr")
    for row in rows[1:]:
        columns = row.find_all('td')
        for column in columns:
            text = column.text
            timer = 0
            increase = True
            target = 'Self'
            if text != 'N/A':
                splited = text.split(' ')
                name = ' '.join(splited[0:2])
                effect = ' '.join(splited[2:])
                effect = effect.replace('(', '').replace(')', '')
                filename = name.lower().replace(' ', '_')
                
                value = re.findall(r'\d+\%?', effect)
                if len(value) == 1:
                    value = value[0]
                elif len(value) == 2:
                    value = value[0]
                    timer = value[1]
                else:
                    value = ''

                if 'reduces' in effect.lower():
                    increase = False
                if 'target' in effect.lower():
                    target = 'Target'

                eff = {
                    'name': name,
                    'effect': effect,
                    'value': value,
                    'timer': timer,
                    'increase': increase,
                    'target': target,
                    'benefit': ''
                }
                with open(f'src/effects/{filename}.json', 'w+', encoding='utf-8') as f:
                    json.dump(eff, f)
    buff = not buff
