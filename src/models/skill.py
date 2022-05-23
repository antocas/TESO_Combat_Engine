# pylint: disable=line-too-long
""" Class character """

import re

from json import loads

class Skill:
    """ Skill """
    def __init__(self, parameter):
        if isinstance(parameter, dict):
            self.attributes = parameter

        elif isinstance(parameter, str):
            name_to_search = parameter.capitalize()
            name_to_search = name_to_search.replace(' ', '_')
            name_to_search = name_to_search + '.json'
            with open(name_to_search, 'r', encoding='utf-8') as file_to_open:
                self.attributes = loads(file_to_open)

    def __str__(self):
        return str(self.attributes)

    def as_dict(self):
        """ Return as dict """
        return self.attributes

    def calculate_coefs(self, max_resource=0, resource_damage=0):
        """ Calculate coefs """
        max_coefs = int(self.attributes['numCoefVars']) + 1
        for n_coef in range(1, max_coefs):
            skill_coef_max_resource = float(self.attributes[f'a{n_coef}'])
            max_resource = int(max_resource)
            skill_coef_resource_damage = float(self.attributes[f'b{n_coef}'])
            resource_damage = int(resource_damage)
            self.attributes[f'userCoef{n_coef}'] = (skill_coef_max_resource * max_resource + skill_coef_resource_damage * resource_damage)
            self.attributes[f'userCoef{n_coef}'] = self.attributes[f'userCoef{n_coef}'] + int(self.attributes[f'userCoef{n_coef}']*(3.3/100))

    @property
    def skill_id(self):
        """ Return id """
        return self.attributes['id']

    @property
    def image(self):
        """ Return image """
        return self.attributes['texture']

    @property
    def skill_type(self):
        """ Return type of skill """
        return self.attributes['skillType']

    @property
    def skill_line(self):
        """ Return skill line name """
        return self.attributes['skillLine']

    @property
    def name(self):
        """ Return name """
        return self.attributes['name']

    @property
    def description(self):
        """ Return fixed description """
        return self.attributes['description']

    @property
    def duration(self):
        """ Return duration """
        return self.attributes['duration']

    @property
    def coef_description(self):
        """ Return description with 'index' for calculated values using coefs """
        return self.attributes['coefDescription']

    @property
    def num_coef_vars(self):
        """ Return number of coeficients """
        return self.attributes['numCoefVars']

    def get_index_attributes(self, index):
        """ Return type_of_damage """
        data = {}
        for key, value in self.attributes.items():
            if key.endswith(index):
                data[key] = value
        return data

    def get_calculated_damage(self):
        """ Calculate the value for each pair of coeficients """
        max_coefs = int(self.attributes['numCoefVars']) + 1
        damage = []
        for i in range(1, max_coefs):
            damage.append(int(self.attributes[f'userCoef{i}']))
        return damage

    def get_calculated_description(self):
        """ Return coef description with $ substituted """
        self.attributes['coef_description_completed'] = re.sub(r'\$\d', '{}', self.attributes['coefDescription'])
