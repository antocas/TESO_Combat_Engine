""" Buff/Debuff generator"""

import re
import json
import requests
from bs4 import BeautifulSoup as bs


raw_page = requests.get('https://eso-u.com/articles/buffs_and_debuffs_the_majorminor_system')
soup = bs(raw_page.content, 'lxml')

tables = soup.find_all("table")
buff = 'buff'
for table in tables[2:]:
    rows = table.find_all("tr")
    for row in rows[1:]:
        columns = row.find_all('td')
        for column in columns:
            stat_affected = []
            text = column.text
            text = text.replace('/', ' and ').lower()
            increase = True
            target = 'Self'
            if text != 'N/A':
                splited = text.split(' ')
                name = ' '.join(splited[0:2]).capitalize()
                effect = ' '.join(splited[2:])
                effect = effect.replace('(', '').replace(')', '')
                filename = name.lower().replace(' ', '_')


                value = re.findall(r'\d+', effect)
                if len(value) == 1:
                    value = value[0]
                elif len(value) == 2:
                    value = value[0]
                else:
                    value = ''

                if '%' in effect:
                    mode = "percent"
                else:
                    mode = "fixed"
                if 'reduces' in effect:
                    increase = False
                if 'target' in effect:
                    target = 'Target'

                pos_stats = [
                    "resistance debuff",
                    "critical damage",
                    "weapon damage",
                    "spell damage",
                    "healing done",
                    "healing received",
                    "damage done",
                    "damage taken",
                    "max health",
                    "critical chance",
                    "physical resistance",
                    "spell resistance",
                    "stamina recovery",
                    "magicka recovery",
                    "health recovery",
                    "mount speed"
                    "speed",
                    "ultimate",
                    "weapon critical",
                    "spell critical",
                    ]

                for words in pos_stats:
                    if all(word in effect for word in words.split(' ')):
                        stat_affected.append(words)
                eff = {
                    'name': name,
                    'effect': effect,
                    'value': value,
                    "mode": mode,
                    'increase': increase,
                    'target': target,
                    'stat_affected': stat_affected
                }

                with open(f'src/effects/{buff}/{filename}.json', 'w+', encoding='utf-8') as f:
                    json.dump(eff, f, indent=4)
    buff = 'debuff'
