""" Class character """

from src.models.character import Character
import re

class Skill:
    def __init__(self, atributes):
        self.attributes = atributes

    def __str__(self):
        return str(self.attributes)

    def as_dict(self):
        return self.attributes

    def calculate_coefs(self, character:Character):
        max_coefs = int(self.attributes['numCoefVars']) + 1
        for n_coef in range(1, max_coefs):
            skill_coef_max_magicka = float(self.attributes[f'a{n_coef}'])
            max_magicka = int(character.max_magicka)
            skill_coef_spell_damage = float(self.attributes[f'b{n_coef}'])
            spell_damage = int(character.spell_damage)
            self.attributes[f'userCoef{n_coef}'] = (skill_coef_max_magicka * max_magicka + skill_coef_spell_damage * spell_damage)
            self.attributes[f'userCoef{n_coef}'] = self.attributes[f'userCoef{n_coef}'] + int(self.attributes[f'userCoef{n_coef}']*(3.3/100))

    @property
    def skill_id(self):
        return self.attributes['id']    

    @property
    def image(self):
        return self.attributes['texture']

    @property
    def skill_type(self):
        return self.attributes['skillType']

    @property
    def skill_line(self):
        return self.attributes['skillLine']

    @property
    def name(self):
        return self.attributes['name']

    @property
    def description(self):
        return self.attributes['description']

    @property
    def coef_description(self):
        return self.attributes['coefDescription']

    def get_calculated_damage(self):
        max_coefs = int(self.attributes['numCoefVars']) + 1
        damage = []
        for i in range(1, max_coefs):
            damage.append( int(self.attributes[f'userCoef{i}']) )
        return damage

    def get_calculated_description(self):
        self.attributes['coef_description'] = re.sub(r'\$\d', '{}', st.session_state['skills_available'][skill_name]['coefDescription'])
