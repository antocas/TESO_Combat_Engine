""" Class character """

class Character:
    def __init__(self, kwargs):
        self.attributes = {
            "name": kwargs.get('name'),
            "health": int(kwargs.get('health')),
            "max_magicka": int(kwargs.get('max_magicka')),
            "max_stamina": int(kwargs.get('max_stamina')),
            "spell_damage": int(kwargs.get('spell_damage')),
            "spell_critical": int(kwargs.get('spell_critical')),
            "spell_penetration": int(kwargs.get('spell_penetration')),
            "physical_damage": int(kwargs.get('physical_damage')),
            "physical_critical": int(kwargs.get('physical_critical')),
            "physical_penetration": int(kwargs.get('physical_penetration')),
            "buffs": kwargs.get('bufs'),
            "debuffs": kwargs.get('debufs'),
            "skill": kwargs.get('skills'),
            "rotation": kwargs.get('rotation')
        }

    def __str__(self):
        return str(self.attributes)

    def as_dict(self):
        return self.attributes

    def apply_buffs():
        pass

    def next_attack(self):
        pass

    def get_name(self):
        return self.attributes["name"]
    def get_spell_damage(self):
        return self.attributes["spell_damage"]
    def get_spell_critical(self):
        return self.attributes["spell_critical"]
    def get_spell_penetration(self):
        return self.attributes["spell_penetration"]
    name = property(get_name)
    spell_damage = property(get_spell_damage)
    spell_critical = property(get_spell_critical)
    spell_penetration = property(get_spell_penetration)
