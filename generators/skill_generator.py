""" Skill generator """

import os
import re
import json
from cv2 import split
import requests
from bs4 import BeautifulSoup as bs


# Print iterations progress
def print_progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', print_end = "\r"):
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
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = print_end)
    # Print New Line on Complete
    if iteration == total:
        print()

def extract_against_raw(coef_string:str, raw_description:str):
    """ New attempt to extract info """
    print(coef_string)
    results = []
    tmp = ''
    split_coef = coef_string.replace('.', '').replace('\n', '').replace('  ', ' ').split(' ')
    split_raw = raw_description.replace('.', '').replace('\n', '').replace('  ', ' ').split(' ')

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
            if tmp != '':
                results.append(tmp[1:])
                tmp = ''
        else:
            tmp = tmp + ' ' + split_coef[c_len]
            if c_len < len_max-1:
                c_len = c_len + 1
            if jump:
                if r_len < len_min-1:
                    jump = False
                    r_len = r_len + 1
    return results

def extract_buff_and_debuff(split:str):
    """ Prepara los buffs y debuffs para la estructura de datos general """
    buff_names = [ s.replace('.json', '').replace('_', ' ').lower() for s in os.listdir('src/effects/buff') ]
    debuff_names = [ s.replace('.json', '').replace('_', ' ').lower() for s in os.listdir('src/effects/debuff') ]
    buffs = []
    debuffs = []
    for buff in buff_names:
        b = buff.split(' ')
        s = f'({b[0]}).*?({b[1]})'
        buff = re.findall(s, split)
        if buff:
            buff = ' '.join(buff[0])
            buffs.append(buff)
    for debuff in debuff_names:
        b = debuff.split(' ')
        s = f'({b[0]}).*?({b[1]})'
        debuff = re.findall(s, split)
        if debuff:
            debuff = ' '.join(debuff[0])
            debuffs.append(debuff)
    return buff, debuffs


def extractor(coef_string:str):
    """ Extract info from coef_string """
    splitted = coef_string.split('. ')

    data = {
        'buffs': [],
        'debuffs': []
    }
    tmp_data = {}

    for selected_split in splitted:
        # print(selected_split)
        split = selected_split.lower()
        if split == '':
            continue

        # Cantidad y tipo de daño
        type_of_damage = re.findall(r'\$\d+ .*? damage', split)
        # Cada cuanto se aplica
        tick_time = [ ''.join(s) for s in re.findall(r'(every|each)( \d+\.?\d* )(second|minute)', split) ]
        # Durante cuanto tiempo se aplica
        duration = [ ''.join(s) for s in re.findall(r'(over|during|for)( \d+\.?\d* )(second|minute)', split) ]
        # Tiempo tras el cual se produce algun efecto
        after = [ ''.join(s) for s in re.findall(r'(after)( \d+\.?\d* )(second|minute)', split) ]
        # Slotable
        slotable_benfit = re.findall(r'while slotted', split)
        # Sinergiable
        synergy = re.findall(r'synergy', split)
        # BUFFS AND DEBUFFS
        buffs, debuffs = extract_buff_and_debuff(split)
        
        if tick_time:
            # print(tick_time)
            multiplier = 1000 if 'second' in tick_time[0] else 3600
            tmp_data['tick_time'] = int(float(re.findall(r'\d+\.?\d*', tick_time[0])[0])*multiplier)
        if duration:
            # print(duration)
            multiplier = 1000 if 'second' in duration[0] else 3600
            tmp_data['duration'] = int(float(re.findall(r'\d+\.?\d*', duration[0])[0])*multiplier)
        if after:
            # print(after)
            multiplier = 1000 if 'second' in after[0] else 3600
            tmp_data['after'] = int(float(re.findall(r'\d+\.?\d*', after[0])[0])*multiplier)
            print(coef_string)
            print(after, tmp_data['after'])

        # Separamos los DATOS
        for buff in buffs:
            data['buffs'].append({
                'effect': buff,
                'duration': tmp_data.get('duration')
            })
        for debuff in debuffs:
            data['debuffs'].append({
                'effect': debuff,
                'duration': tmp_data.get('duration')
            })
        
        if type_of_damage:
            number_type = re.findall(r'\d+', type_of_damage[-1])[0]
            data[f'tick{number_type}'] = tmp_data.get('tick_time')
            data[f'duration{number_type}'] = tmp_data.get('tick_time')
            data[f'after{number_type}'] = tmp_data.get('tick_time')
            data[f'synergy{number_type}'] = bool(synergy)
            data[f'sloteable{number_type}'] = bool(slotable_benfit)
        
        return data

raw_page = requests.get('https://esoitem.uesp.net/viewSkills.php')
soup = bs(raw_page.content, 'lxml')

base_skill_url = 'https://esoitem.uesp.net/viewlog.php?action=view&record=minedSkills&id='

skills = soup.find_all("div", {"class": "esovsAbilityBlockHover"})
i_ = 0

for iter, skill in enumerate(skills):
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

    if skill_dict.get('coefDescription'):
        data_extracted = extractor(skill_dict['coefDescription'])
        skill_dict.update(data_extracted)


    print(extract_against_raw(skill_dict.get('description'), skill_dict.get('rawDescription')))
    continue
    # i_ = i_+ 1
    # if i_ == 50:
    #     break
    # print('*************************************************************************************************\n')
    file_name = 'src/skills/'+skill_dict['name']+'.json'
    with open(file_name.replace(' ', '_'), 'w+', encoding='utf-8') as f:
        json.dump(skill_dict, f, indent=4)
    print_progress_bar(iter, 1473)
    i_ = iter
print(i_)
