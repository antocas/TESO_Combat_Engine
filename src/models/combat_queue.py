""" Queue for attacks """
from copy import deepcopy
from src.models import attack

class QueueAttack:
    """ Queue for attacks """
    def __init__(self):
        """ Queue for attacks """
        self._attacks = {}
        self._to_remove = []

    def __str__(self):
        at = [ name for name, attack in self._attacks.items() ]
        return ', '.join(at)

    def add_attack(self, attack:attack.Attack):
        """ Add to queue """
        self._attacks[attack._name] = deepcopy(attack)

    def decrease_attack_duration(self, attack_name:str, channeling_time:int=1):
        """ Remove from queue """
        self._attacks[attack_name]._duration = self._attacks[attack_name]._duration - channeling_time
        if self._attacks[attack_name]._duration == 0:
            self._to_remove.append(attack_name)

    def clear_attacks(self):
        """ Remove those attacks which finished recently """
        # Revisamos los ataques y si tienen duracion o ha caducado
        while len(self._to_remove) > 0:
            name = self._to_remove.pop()
            del self._attacks[name]

    def in_queue(self, name):
        """ Checks if some attack it's in queue """
        return name in self._attacks
