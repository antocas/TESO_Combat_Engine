""" Passive extractor, aims to reduce the scalability difficulty """
import os
import re
import json

def whiles_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(while)(.*? )(in combat|ability slotted|negative effect)'
    while_options = re.findall(while_pattern, passive_description, re.IGNORECASE)
    if len(while_options) > 0:
        return [option[-1] for option in while_options]
    else:
        return None

def restores_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = re.compile(r'(restores)')
    while_combat = re.findall(while_pattern, passive_description)
    return bool(while_combat)

def weapon_dependent_regex(passive_descheader):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(with )(.*?)( equipped)'
    while_combat = re.findall(while_pattern, passive_descheader, re.IGNORECASE)
    if while_combat:
        return while_combat[0][1].lower()
    else:
        return False

def armor_dependent_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(for each piece of )(.*?)( equipped|\.| worn)'
    while_combat = re.findall(while_pattern, passive_description, re.IGNORECASE)
    if while_combat:
        return while_combat[0][1].lower()
    else:
        return False

def ability_slotted_dependent_regex(passive_description):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = r'(for each )(.*?)( ability slotted)'
    while_combat = re.findall(while_pattern, passive_description, re.IGNORECASE)
    if while_combat:
        return while_combat[0][1].lower()
    else:
        return False


def extract_benefits(passive_description):
    """ Extracts passive benefits from passive description """
    phrases = passive_description.split('. ')
    for phrase in phrases:
        if 'increase' in phrase:
            pattern = r'increase.*by \d+%?'
            p = re.findall(pattern, phrase)
    return ''



for passive_name in os.listdir('src/skills/passive'):
    with open(f"src/skills/passive/{passive_name}", "r", encoding="utf-8") as file:
        passive = json.load(file)
        data = {}
        description = passive['description'].lower()
        description = re.sub(' +', ' ', description)
        data["weapon_dependent"] = weapon_dependent_regex(passive["descHeader"])
        data["armor_dependent"] = armor_dependent_regex(passive["description"])
        data["ability_slotted_dependent"] = ability_slotted_dependent_regex(passive["description"])
        data["while"] = whiles_regex(passive['description'])
        data["restores"] = restores_regex(passive['description'])
        data["benefits"] = extract_benefits(passive['description'])
        print(data)
