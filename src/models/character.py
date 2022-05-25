# pylint: disable=unused-import
""" Class character """
from copy import deepcopy

from json import load, dumps
from src.models.skill import Skill

class Character:
    """ Character """
    def __init__(self, atributes):
        self.attributes = atributes
        self.attributes['skills'] = {}
        self.attributes['passives'] = {}
        # Load skills and passives
        if self.attributes.get('skills_available'):
            self.__load_skills__()
        if self.attributes.get('passives_available'):
            self.__load_passives__()
        # Apply buffs
        self.apply_buffs()

    def __str__(self):
        return str(self.attributes)

    def as_dict(self):
        """ Return as dict """
        return self.attributes

    def __load_skills__(self):
        """ Load skill from file """
        for skill_name in self.attributes['skills_available']:
            skill_file_name = skill_name.lower().replace(' ', '_')
            for type_of_skill in ['ultimate', 'skill']:
                try:
                    with open(f'src/skills/{type_of_skill}/{skill_file_name}.json', 'r', encoding='utf-8') as file:
                        skill = load(file)
                        self.attributes['skills'][skill_name] = Skill(skill)
                except FileNotFoundError:
                    continue

    def __load_passives__(self):
        """ Load skill from file """
        for passive_name in self.attributes['passives_available']:
            passive_file_name = passive_name.lower().replace(' ', '_')
            with open(f'src/skills/passive/{passive_file_name}.json', 'r', encoding='utf-8') as file:
                passive = load(file)
                self.attributes['passives'][passive_name] = Skill(passive)

    def apply_buffs(self):
        """ Apply buffs to the character """
        for passive in self.attributes['passives']:
            continue
            print(passive)
        return None

    def next_attack(self):
        """ Return next attack """
        return None

    def savable(self):
        """ Converts into small dict, db friendly """
        character = deepcopy(self.attributes)
        del character['skills']
        del character['passives']
        return character

    def apply_passives(self):
        """ Apply passives """
        return None

    def get_skill(self, skill_name: str):
        """ Return skill """
        return self.attributes['skills'][skill_name]


    @property
    def name(self):
        """ Return name """
        return self.attributes.get("name") or ""

    @property
    def max_magicka(self):
        """ Return max magicka """
        return self.attributes.get("max_magicka") or 0

    @property
    def max_stamina(self):
        """ Return max stamina """
        return self.attributes.get("max_stamina") or 0

    @property
    def class_name(self):
        """ Return class name """
        return self.attributes.get("class") or ""

    @property
    def spell_damage(self):
        """ Return spell damage """
        return self.attributes.get("spell_damage") or 0

    @property
    def weapon_damage(self):
        """ Return weapon damage """
        return self.attributes.get("weapon_damage") or 0

    @property
    def spell_critical(self):
        """ Return spell critical """
        return self.attributes.get("spell_critical") or 0

    @property
    def weapon_critical(self):
        """ Return spell critical """
        return self.attributes.get("weapon_critical") or 0

    @property
    def spell_penetration(self):
        """ Return spell penetration """
        return self.attributes.get("spell_penetration") or 0

    @property
    def main_bar(self):
        """ Return main bar """
        return self.attributes.get("main_bar") or ""

    @property
    def second_bar(self):
        """ Return second bar """
        return self.attributes.get("second_bar") or ""

    @property
    def rotation(self):
        """ Return rotation """
        return self.attributes.get("rotation") or []

    @property
    def critical_chance(self):
        """ Return critical chance """
        return self.attributes.get("critical_chance") or []
