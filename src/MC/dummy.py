""" Dummy class """

from copy import deepcopy
from src.MC.effects import Effect


class Dummy:
    """ Dummy class """
    def __init__(self, kwargs):
        """ Dummy class """
        self.attributes = {
            "name": kwargs.get('name') or "Iron Atronach",
            "health_bar": kwargs.get('health') or 21000000, #21M Dummy
            "debuffs": kwargs.get('debuffs') or {},
            "base_resistance": kwargs.get('base_armor') or 18200, # Standard armor
            "spell_resistance": kwargs.get('base_armor') or 18200,
            "physical_resistance": kwargs.get('base_armor') or 18200,
            "damage_extra": 0,
            "critical_damage_extra": 0
        }

    def __str__(self) -> str:
        """ Str dummy """
        print("Health bar:", self.attributes["health_bar"])
        print("Debufs")
        # print(self.attributes["debufs"])
        return "Dummy class"

    def hit_dummy(self, damage, penetration, type_of_damage='spell_resistance', critical_damage=False):
        """ Calculate damage received by the dummy """
        # Aplicamos los debufos contra la armadura
        armor = self.attributes[type_of_damage]
        armor = armor - penetration
        mitigation = self.__calculate_mitigation__()
        total_damage = damage * (1 - mitigation)
        self.attributes["health_bar"] = self.attributes["health_bar"] - total_damage

    def __calculate_mitigation__(self, type_of_damage="spell_resistance"):
        """ Calculate mitigation """
        percent = 0.5/25000
        return max(0, self.attributes[type_of_damage]*percent)

    def set_debuff(self, debuf: Effect):
        """ Set some debuf to the dummy """
        effect_name = debuf.name
        debuf_copy = deepcopy(debuf)
        self.attributes['debuffs'][effect_name] = debuf_copy

    def apply_debuffs(self):
        """ Apply debuffs on dummy """
        # In order to apply correctly, we separate the logic from the main "combat"
        # So, first we apply debuffs (some ignored, it's a freaking dummy), then we hit the dummy
        remove = []
        for name, debuff in self.attributes['debuffs'].items():
            # print(debuff)
            if debuff.mode == 'percent':
                stat = (self.attributes[ debuff.stat_affected ] * debuff.value) // 100
            elif debuff.mode == 'fixed':
                stat = debuff.value
            print(name, debuff)
            self.attributes[ debuff.stat_affected ] = max(0, self.attributes[ debuff.stat_affected ] - stat)
            try:
                debuff.decrease_duration()
                if debuff.duration == 0:
                    remove.append(name)
            except:
                pass
            # print(name, debuff.stat_affected, self.attributes[ debuff.stat_affected])
        for name in remove:
            del self.attributes['debuffs'][name]

    def reset_resistances(self):
        self.attributes['spell_resistance'] = self.attributes["base_resistance"]
        self.attributes['physical_resistance'] = self.attributes["base_resistance"]

    def as_dict(self):
        data = {
            "name": self.attributes['name'],
            "health_bar": self.attributes['health_bar'],
            "base_resistance": self.attributes['base_resistance'],
            "spell_resistance": self.attributes['spell_resistance'],
            "physical_resistance": self.attributes['physical_resistance'],
            "damage_extra": 0,
            "critical_damage_extra": 0
        }
        return data

    def get_health(self):
        return self.attributes['health_bar']

    health = property(get_health)