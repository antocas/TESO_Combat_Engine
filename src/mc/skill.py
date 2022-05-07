""" Class character """

from src.mc.character import Character


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
