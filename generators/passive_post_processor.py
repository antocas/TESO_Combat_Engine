""" Passive extractor, aims to reduce the scalability difficulty """

import re
import json

def whiles_regex(passive):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = re.compile(r'(while in combat)')
    while_combat = re.findall(while_pattern, passive)
    if while_combat:
        passive = passive.replace(while_combat[0], 'combat')
    return passive

def restores_regex(passive):
    """ Tries to simplify all while in combat, while in combat, while restoration staff equiped """
    while_pattern = re.compile(r'(while in combat)')
    while_combat = re.findall(while_pattern, passive)
    if while_combat:
        passive = passive.replace(while_combat[0], 'combat')
    return passive