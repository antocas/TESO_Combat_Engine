# pylint: disable=invalid-name
# pylint: disable=multiple-statements
""" Passive extractor, aims to reduce the scalability difficulty """
import os
import re
import sys
import json

import colored

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
        return {'depends_on_weapon': while_combat[0][1]}
    return {}

def armor_dependent_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(each piece of |bonus based on the type of )(.*?)( equipped|\.| worn| does)'
    while_combat = re.findall(while_pattern, passive_description)
    if while_combat:
        return {'armor_bonus': while_combat[0][1]}
    return {}

def ability_slotted_dependent_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(for each |while you have a )(.*?)( ability)?( )(slotted|active)'
    while_combat = re.findall(while_pattern, passive_description)
    if while_combat:
        return {f'ability_{while_combat[0][4]}': while_combat[0][1]}
    return {}

def ability_used_dependent_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(when )(.*?)( with a )(.*?)( ability)'
    while_combat = re.findall(while_pattern, passive_description)
    if while_combat:
        return {'ability_used': while_combat[0][3]}
    return {}

def extract_benefits_percent(passive_description):
    """ Extracts passive benefits from passive description """
    inner_data = []
    passive_description = passive_description.replace(':', '.')
    passive_description = passive_description.replace('  ', '. ')
    phrases = passive_description.split('. ')

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

if __name__=='__main__':
    DEBUG = bool(len(sys.argv) == 2 and sys.argv[1].lower() == 'debug')
    new_keywords = set()
    list_of_keywords = []

    for passive_name in os.listdir('src/skills/passive'):
        with open(f"src/skills/passive/{passive_name}", "r", encoding="utf-8") as file:
            passive = json.load(file)

        data = {}
        description = passive['description'].lower()
        # description = re.sub(' +', ' ', description)
        data.update(weapon_dependent_regex(passive["descHeader"].lower()))
        data.update(armor_dependent_regex(description))
        data.update(ability_slotted_dependent_regex(description))
        data.update(whiles_regex(description))
        data.update(restores_regex(description))
        data.update(ability_used_dependent_regex(description))
        benefits = extract_benefits_percent(description)
        if benefits:
            data['benefits'] = benefits
        if DEBUG: print(colored.bg(147), passive['name'], colored.bg(32), description, colored.attr(0))
        if (DEBUG and data): print(colored.bg(34), data, colored.attr(0))
        if DEBUG: print("\n")
        list_of_keywords = list_of_keywords + (list(data.keys()))
        data.update(passive)

        if not DEBUG:
            with open(f"src/skills/passive/{passive_name}", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
    if not DEBUG: print(set(list_of_keywords))
