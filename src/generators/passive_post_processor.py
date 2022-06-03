# pylint: disable=invalid-name
""" Passive extractor, aims to reduce the scalability difficulty """
import os
import re
import json

import colored
DEBUG=0

def whiles_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(while)(.*? )(in combat|ability slotted|negative effect)'
    while_options = re.findall(while_pattern, passive_description)
    return {option[-1]:True for option in while_options}

def restores_regex(passive_description):
    """ Tries to simplify all potential benefits """
    while_pattern = re.compile(r'(restores)')
    while_combat = re.findall(while_pattern, passive_description)
    if while_combat:
        return {while_combat[0]: True}
    return {}

def weapon_dependent_regex(passive_descheader):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(with )(.*?)( equipped)'
    while_combat = re.findall(while_pattern, passive_descheader)
    if while_combat:
        return {while_combat[0][1].lower():True}
    return {}

def armor_dependent_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(each piece of |bonus based on the type of )(.*?)( equipped|\.| worn| does)'
    while_combat = re.findall(while_pattern, passive_description)
    if while_combat:
        bonus = while_combat[0][1].lower() + ' bonus'
        return {bonus:True}
    return {}

def ability_slotted_dependent_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(for each )(.*?)( ability slotted)'
    while_combat = re.findall(while_pattern, passive_description)
    if while_combat:
        return {while_combat[0][1].lower(): True}
    return {}


def extract_benefits_percent(passive_description):
    """ Extracts passive benefits from passive description """
    inner_data = []
    passive_description = passive_description.replace(':', '.')
    passive_description = passive_description.replace('  ', '. ')
    phrases = passive_description.split('. ')
    if DEBUG: print(colored.fg(2), phrases, colored.attr(0))
    for phrase in phrases:
        pattern = r'(increase|decrease|reduce)(s? )(.*?)(from |the |with |your )(.*?)( by )(\d+%?)'
        benefit = re.findall(pattern, phrase)
        if benefit:
            for i in benefit:
                mid_step=[]
                mid_step.append(i[0])
                if i[2] != '':
                    mid_step.append(i[2][:-1])
                s = i[3].split('and')
                for j in s:
                    pattern = r'(increase|decrease|reduce)(s?)( your)?(.*?)( by )(\d+%?)'
                    b = re.findall(pattern, j)
                    if b:
                        mid_step.append(b)
                if i[4] != '':
                    mid_step.append(i[4])
                mid_step.append(i[6])
                inner_data.append(mid_step)
    return inner_data


for passive_name in os.listdir('src/skills/passive'):
    with open(f"src/skills/passive/{passive_name}", "r", encoding="utf-8") as file:
        passive = json.load(file)

    data = passive
    description = passive['description'].lower()
    # description = re.sub(' +', ' ', description)
    data.update(weapon_dependent_regex(passive["descHeader"]))
    data.update(armor_dependent_regex(description))
    data.update(ability_slotted_dependent_regex(description))
    data.update(whiles_regex(description))
    data.update(restores_regex(description))
    benefits = extract_benefits_percent(description)
    if benefits:
        data['benefits'] = benefits
    if DEBUG: print(colored.bg(147), passive['name'], colored.attr(0), description, data)

    if not DEBUG:
        with open(f"src/skills/passive/{passive_name}", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
