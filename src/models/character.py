# pylint: disable=unused-import
""" Class character """
from copy import deepcopy

from json import load, dumps
import os
import re
from src.models.skill import Skill
from src.models.effects import Effect
class Character:
    """ Character """
    def __init__(self, atributes):
        tmp_buffs = {}
        tmp_debuffs = {}

        self.attributes = atributes
        self.attributes['skills'] = {}
        self.attributes['passives'] = {}
        # Load skills and passives
        if self.attributes.get('skills_available'):
            self.__load_skills__()
        if self.attributes.get('passives_available'):
            self.__load_passives__()
        for buff in self.attributes['buffs']:
            tmp_buffs[buff] = Effect.open_as_effect(buff, 'buff')
        for debuff in self.attributes['debuffs']:
            tmp_debuffs[debuff] = Effect.open_as_effect(debuff, 'debuff')
        self._buffs = tmp_buffs
        self.attributes['debuffs'] = tmp_debuffs

        # Apply buffs
        self.apply_buffs()

    def __str__(self):
        return str(self.attributes)

    def as_dict(self):
        """ Return as dict """
        return self.attributes

    def __load_skills__(self):
        """ Load skill from file """
        list_of_skills = os.listdir('src/skills/skill')
        print(list_of_skills)
        for skill_name in self.attributes['skills_available']:
            skill_file_name = skill_name.lower().replace(' ', '_')
            skill_file_name = skill_file_name + '.json'
            print(skill_file_name)
            file_name = [name for name in list_of_skills if name.endswith(skill_file_name)]
            print(file_name)
            if len(file_name)>0:
                try:
                    with open(f'src/skills/skill/{file_name[0]}', 'r', encoding='utf-8') as file:
                        skill = load(file)
                        self.attributes['skills'][skill_name] = Skill(skill)
                        print(self.attributes['skills'])
                except FileNotFoundError:
                    continue

    def __load_passives__(self):
        """ Load skill from file """
        list_of_skills = os.listdir('src/skills/passive')
        for skill_name in self.attributes['passives_available']:
            skill_file_name = skill_name.lower().replace(' ', '_')
            file_name = [name for name in list_of_skills if name.endswith(skill_file_name)]
            if len(file_name)>0:
                try:
                    with open(f'src/skills/passives_available/{file_name[0]}', 'r', encoding='utf-8') as file:
                        skill = load(file)
                        self.attributes['passives'][skill_name] = Skill(skill)
                except FileNotFoundError:
                    continue

    def __load_ultimates__(self):
        """ Load skill from file """
        list_of_skills = os.listdir('src/skills/ultimate')
        for skill_name in self.attributes['skills_available']:
            skill_file_name = skill_name.lower().replace(' ', '_')
            file_name = [name for name in list_of_skills if name.endswith(skill_file_name)]
            if len(file_name)>0:
                try:
                    with open(f'src/skills/ultimates_available/{file_name[0]}', 'r', encoding='utf-8') as file:
                        skill = load(file)
                        self.attributes['skills'][skill_name] = Skill(skill)
                except FileNotFoundError:
                    continue

    def apply_buffs(self):
        """ Apply buffs to the character """
        self._damage_done = 0
        self._critical_damage_done = 0
        self._weapon_damage_added = 0
        self._spell_damage_added = 0
        self._weapon_critical_added = 0
        self._spell_critical_added = 0
        for _, buff in self._buffs.items():
            if "critical damage" in buff.stat_affected:
                self._critical_damage_done = self._critical_damage_done + int(buff.value)
            if "damage done" in buff.stat_affected:
                self._damage_done = self._damage_done + int(buff.value)
            if "weapon damage" in buff.stat_affected:
                self._weapon_damage_added = self._weapon_damage_added + int(buff.value)
            if "spell damage" in buff.stat_affected:
                self._spell_damage_added = self._spell_damage_added + int(buff.value)
            if "weapon critical" in buff.stat_affected:
                self._weapon_critical_added = self._weapon_critical_added + int(buff.value)
            if "spell critical" in buff.stat_affected:
                self._spell_critical_added = self._spell_critical_added + int(buff.value)

    def savable(self):
        """ Converts into small dict, db friendly """
        character = deepcopy(self.attributes)
        skills = [skill['name'] for skill in character.attributes['skills']]
        passives = [skill['name'] for skill in character.attributes['passives']]
        print(skills, passives)
        del character['skills']
        del character['passives']
        return character

    def apply_passives(self):
        """ Apply passives """
        # ! Probablemente sea sencillo coger las pasivas y chutarlas a la parte de los buffs
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
        return int(self.attributes["spell_damage"]) + self._spell_damage_added

    @property
    def weapon_damage(self):
        """ Return weapon damage """
        return int(self.attributes["weapon_damage"]) + self._weapon_damage_added

    @property
    def spell_critical(self):
        """ Return spell critical """
        return int(self.attributes["spell_critical"]) + self._spell_critical_added + self.critical_damage_done

    @property
    def weapon_critical(self):
        """ Return spell critical """
        return int(self.attributes["weapon_critical"]) + self._weapon_critical_added + self.critical_damage_done

    @property
    def damage_done(self):
        """ Return damage added from buffs """
        return self._damage_done/100.0

    @property
    def critical_damage_done(self):
        """ Return critical damage added from buffs """
        return self._critical_damage_done/100.0


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
        return float(self.attributes.get("critical_chance")) or 0.0
