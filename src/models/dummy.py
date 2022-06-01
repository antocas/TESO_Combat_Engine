# pylint: disable=line-too-long
""" Dummy class """

from copy import deepcopy
from src.models.effects import Effect


class Dummy:
    """ Dummy class """
    def __init__(self, kwargs):
        """ Dummy class """
        tmp_buffs = {}
        tmp_debuffs = {}
        self.attributes = kwargs
        for buff in self.attributes['buffs']:
            tmp_buffs[buff] = Effect.open_as_effect(buff, 'buff')
        for debuff in self.attributes['debuffs']:
            tmp_debuffs[debuff] = Effect.open_as_effect(debuff, 'debuff')
        self.attributes['buffs'] = tmp_buffs
        self.attributes['debuffs'] = tmp_debuffs
        self.attributes["spell_resistance"] = kwargs.get('base_resistance')
        self.attributes["physical_resistance"] = kwargs.get('base_resistance')

        # * Set percent of extra damage for this round
        self.damage_taken = 0
        self.critical_damage_taken = 0

    def __str__(self) -> str:
        """ Str dummy """
        return str(self.attributes)

    def hit_dummy(self, damage, penetration, type_of_damage='spell_resistance', critical_damage=False):
        """ Calculate damage received by the dummy """
        # Aplicamos los debufos contra la armadura
        armor = self.attributes[type_of_damage]
        armor = armor - penetration
        mitigation = self.__calculate_mitigation__(armor)
        total_damage = int(damage * (1 - mitigation))
        if not critical_damage:
            # * Increase damage received by debuffs
            total_damage = int(total_damage * (1 + self.damage_taken))
        else:
            # * Increase critical damage received by debuffs
            total_damage = int(total_damage * (1 + self.critical_damage_taken))
        self.attributes["health"] = self.attributes["health"] - total_damage
        return total_damage

    @classmethod
    def __calculate_mitigation__(cls, armor):
        """ Calculate mitigation """
        percent = 0.5/25000
        return max(0, armor*percent)

    def set_debuff(self, debuf: Effect):
        """ Set some debuf to the dummy """
        effect_name = debuf.name
        debuf_copy = deepcopy(debuf)
        self.attributes['debuffs'][effect_name] = debuf_copy

    def apply_debuffs(self):
        """ Apply debuffs on dummy """
        # In order to apply correctly, we separate the logic from the main "combat"
        # So, first we apply debuffs (some ignored, it's a freaking dummy), then we hit the dummy
        self.attributes['spell_resistance'] = self.attributes["base_resistance"]
        self.attributes['physical_resistance'] = self.attributes["base_resistance"]
        self.damage_taken  = 0
        self.critical_damage_taken = 0
        remove = []
        for name, debuff in self.attributes['debuffs'].items():
            # ! Daño recibido
            if 'damage taken' in debuff.stat_affected:
                self.damage_taken = self.damage_taken + int(debuff.value)/100.0
            if 'critical damage' in debuff.stat_affected:
                self.critical_damage_taken = self.critical_damage_taken + int(debuff.value)/100.0
            if 'resistance debuff' in debuff.stat_affected:
                self.attributes["spell_resistance"] = max(0, self.attributes["spell_resistance"] - int(debuff.value))
                self.attributes["physical_resistance"] = max(0, self.attributes["physical_resistance"] - int(debuff.value))

            debuff.decrease_duration()
            if debuff.duration == 0:
                remove.append(name)
        for name in remove:
            del self.attributes['debuffs'][name]

    def as_dict(self):
        """ Return as dictionary """
        return self.attributes

    @property
    def health(self):
        """ Return health """
        return self.attributes['health']
