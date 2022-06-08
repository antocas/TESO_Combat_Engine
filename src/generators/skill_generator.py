# pylint: disable=import-error
# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
""" Skill generator """

import os
import re
import sys
import json

from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup as bs


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    progress_bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{progress_bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()

def extract_against_raw(coef_string: str, raw_description: str):
    """ New attempt to extract info """
    pre_coef = re.sub(' +', ' ', coef_string)
    pre_raw = re.sub('\n', ' ', raw_description)
    pre_raw = re.sub(' +', ' ', pre_raw)
    print('Coef:', pre_coef, '\n')
    print("Raw:", pre_raw, '\n')

    results = {}
    tmp_coef = ''
    tmp_raw = ''
    split_coef = pre_coef.split(' ')
    split_raw = pre_raw.split(' ')

    len_max = max(len(split_coef), len(split_raw))
    len_min = min(len(split_coef), len(split_raw))
    c_len = 0
    r_len = 0
    jump = True
    while c_len < len_max-1 and r_len < len_max-1:
        # print(len_max, len_min, c_len, r_len, split_coef[c_len], split_raw[r_len])

        if split_coef[c_len] == split_raw[r_len]:
            c_len = c_len + 1
            r_len = r_len + 1
            jump = True
            if tmp_coef != '':
                data = { re.findall(r'<<\d+>>', tmp_raw)[0]: tmp_coef[1:] }
                results.update(data)
                tmp_coef = ''
                tmp_raw = ''
        else:
            tmp_coef = tmp_coef + ' ' + split_coef[c_len]
            tmp_raw = tmp_raw + ' ' + split_raw[r_len]
            if c_len < len_max-1:
                c_len = c_len + 1
            if jump:
                if r_len < len_min-1:
                    jump = False
                    r_len = r_len + 1
    return results

def extract_effect(phrase: str, type_of_effect: str):
    """ Prepara los buffs y debuffs para la estructura de datos general """
    effect_names = [s.replace('.json', '').replace('_', ' ').lower() for s in os.listdir(f'src/effects/{type_of_effect}')]
    effects = []
    for effect in effect_names:
        splited_buff = effect.split(' ')
        buff_pattern = f'({splited_buff[0]}).*?({splited_buff[1]})'
        eff = re.findall(buff_pattern, phrase)
        if eff:
            effs = ' '.join(eff[0])
            effects.append(effs)
    return effects

def extractor(skill_dict: dict):
    """ Extract info from coef_string """
    if skill_dict.get('coefDescription') and skill_dict['coefDescription'] != '':
        coef_string = skill_dict['coefDescription']
    else:
        coef_string = skill_dict['description']

    splitted = coef_string.split('$')
    splitted_by_dolar = [splitted[0]]+[ '$'+c for c in splitted[1:] ]
    splitted_flatted = [ c for sub in splitted_by_dolar for c in re.split(r'\. +', sub) ]

    data = {
        'buffs': [],
        'debuffs': []
    }

    for selected_split in splitted_flatted:
        split = selected_split.lower()
        tmp_data = {}
        if split == '':
            continue

        # Cantidad y tipo de daño
        type_of_damage = re.findall(r'\$\d+ \w*? damage', split)
        # Cada cuanto se aplica
        tick_time = [''.join(s) for s in re.findall(r'(every|each)( \d+\.?\d* )(second|minute)', split)]
        # Durante cuanto tiempo se aplica
        duration = [''.join(s) for s in re.findall(r'(over|during|for)( \d+\.?\d* )(second|minute)', split)]
        # Tiempo tras el cual se produce algun efecto
        after = [''.join(s) for s in re.findall(r'(after)( \d+\.?\d* )(second|minute)', split)]
        # Slotable
        slotable_benfit = re.findall(r'while slotted', split)
        # Sinergiable
        synergy = re.findall(r'synergy', split)
        # BUFFS AND DEBUFFS
        buffs = extract_effect(split, 'buff')
        debuffs = extract_effect(split, 'debuff')

        if tick_time:
            # print(tick_time)
            multiplier = 1000 if 'second' in tick_time[0] else 3600
            tmp_data['tick_time'] = int(float(re.findall(r'\d+\.?\d*', tick_time[0])[0])*multiplier)
        if duration:
            multiplier = 1000 if 'second' in duration[0] else 3600
            tmp_data['duration'] = int(float(re.findall(r'\d+\.?\d*', duration[0])[0])*multiplier)

        if after:
            # print(after)
            multiplier = 1000 if 'second' in after[0] else 3600
            tmp_data['after'] = int(float(re.findall(r'\d+\.?\d*', after[0])[0])*multiplier)

        if tmp_data.get('tick_time') and tmp_data['tick_time'] != 0:
            if (tmp_data.get('duration') and tmp_data['duration'] == 0) or tmp_data.get('duration') is None:
                tmp_data['duration'] = skill_dict['duration']

        if duration and 'over' in duration[0]:
            tmp_data['duration_over'] = tmp_data["duration"]/multiplier
        else:
            tmp_data['duration_over'] = 1

        # Separamos los DATOS
        for buff in buffs:
            if buff != 'n and':
                data['buffs'].append({
                    'effect': buff,
                    'duration': tmp_data.get('duration') or skill_dict['duration']
                })
        for debuff in debuffs:
            if debuff != 'n and':
                data['debuffs'].append({
                    'effect': debuff,
                    'duration': tmp_data.get('duration') or skill_dict['duration']
                })

        if type_of_damage:
            number_type = re.findall(r'\d+', type_of_damage[-1])[0]
            data[f'type_of_damage_{number_type}'] = type_of_damage[0][3:]
            data[f'tick_{number_type}'] = tmp_data.get('tick_time') or 0
            data[f'duration_{number_type}'] = tmp_data.get('duration') or 0
            data[f'after_{number_type}'] = tmp_data.get('after') or 0
            data[f'synergy_{number_type}'] = bool(synergy) or False
            data[f'sloteable_{number_type}'] = bool(slotable_benfit) or False
            tick_time = data[f'tick_{number_type}'] or int(skill_dict['tickTime']) or 1000
            over_time = tmp_data['duration_over'] or 1
            data[f'a{number_type}_scaled'] = float(skill_dict[f"a{number_type}"])/over_time * (1000/float(tick_time))
            data[f'b{number_type}_scaled'] = float(skill_dict[f"b{number_type}"])/over_time * (1000/float(tick_time))
            data[f'c{number_type}_scaled'] = float(skill_dict[f"c{number_type}"])/over_time * (1000/float(tick_time))
    return data

def get_skill(skill_id):
    """ Extract info from one skill """
    base_skill_url = 'https://esoitem.uesp.net/viewlog.php?action=view&record=minedSkills&id='

    url = base_skill_url + skill_id
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

    data_extracted = extractor(skill_dict)

    skill_dict.update(data_extracted)
    return skill_dict

def mp_get_skill(skill_id):
    """ Extract info from one skill """
    skill_dict = get_skill(skill_id)
    sk_name = f"{skill_dict['id']}_{skill_dict['name'].lower()}"
    if skill_dict['isPassive'] == "1":
        slot_pass = 'passive'
    elif (skill_dict['mechanic'] == "Ultimate" or skill_dict['mechanic'] == "Adrenaline") and (int(skill_dict['cost']) > 0 and int(skill_dict['cost']) <= 500):
        slot_pass = 'ultimate'
    else:
        slot_pass = 'skill'
    file_name = f'src/skills/{slot_pass}/{sk_name}.json'
    with open(file_name.replace(' ', '_'), 'w+', encoding='utf-8') as file_:
        json.dump(skill_dict, file_, indent=4)

def mp_all_skills():
    """ Loop for all skills """
    with Pool(8) as pool:
        raw_page = requests.get('https://esoitem.uesp.net/viewSkills.php')
        soup = bs(raw_page.content, 'lxml')

        skills = soup.find_all("div", {"class": "esovsAbilityBlockHover"})
        skills_ids = [skill_id.get('skillid') for skill_id in skills]
        print("Starting")
        pool.map(mp_get_skill, skills_ids)

if __name__=='__main__':
    if len(sys.argv) == 2:
        elements = ["41711", "27167", "42529", "36234", "42747"]
        for element in elements:
            r = get_skill(element)
            to_print = json.dumps(r, indent=4)
            print(to_print)
    else:
        mp_all_skills()
