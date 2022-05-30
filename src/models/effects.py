""" Effect class """

import json

class Effect:
    """ Effect class """
    def __init__(self, kwargs: dict, duration: int):
        """ Effect class """
        self.__attributes__ = kwargs
        self.__attributes__['duration'] = duration

    def __str__(self) -> str:
        """ Str effect """
        string = f'Name: {self.__attributes__["name"]}\nValue: {self.__attributes__["value"]}\nStat affected {self.__attributes__["stat_affected"]}\nMode: {self.__attributes__["mode"]}\nDuration: {self.__attributes__["duration"]}\nType: {self.__attributes__["type"]}\n'
        return string

    def decrease_duration(self):
        """ Decrease duration """
        self.__attributes__["duration"] -= 1000

    @classmethod
    def open_as_effect(cls, name: str, effect_type: str, duration=9999999999):
        """ Open effect """
        effect_name = name.lower().replace(' ', '_')
        with open(f"src/effects/{effect_type}/{effect_name}.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return Effect(data, duration)

    @property
    def name(self):
        """ Return name """
        return self.__attributes__["name"]

    @property
    def value(self):
        """ Return value """
        return self.__attributes__["value"]

    @property
    def mode(self):
        """ Return mode """
        return self.__attributes__["mode"]

    @property
    def duration(self):
        """ Return duration """
        return self.__attributes__["duration"]

    @property
    def increase(self):
        """ Return increase """
        return self.__attributes__["increase"]

    @property
    def target(self):
        """ Return target """
        return self.__attributes__["target"]

    @property
    def stat_affected(self):
        """ Return stat_affected """
        return self.__attributes__["stat_affected"]
