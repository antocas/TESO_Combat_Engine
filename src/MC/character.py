""" Class character """

class Character:
    def __init__(self, **kwargs):
        self.attributes = {
            "name": kwargs.get('name'),
            "health": kwargs.get('health'),
            "max_magicka": kwargs.get('max_magicka'),
            "max_stamina": kwargs.get('max_stamina'),
            "spell_damage": kwargs.get('spell_damage'),
            "spell_critical": kwargs.get('spell_critical'),
            "spell_penetration": kwargs.get('spell_penetration'),
            "physical_damage": kwargs.get('physical_damage'),
            "physical_critical": kwargs.get('physical_critical'),
            "physical_penetration": kwargs.get('physical_penetration'),
            "buffs": kwargs.get('bufs'),
            "debuffs": kwargs.get('debufs'),
            "skill": kwargs.get('skills'),
            "rotation": kwargs.get('rotation')
        }

    def 
