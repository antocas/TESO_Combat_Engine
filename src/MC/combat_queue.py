""" Queue for attacks """
from copy import deepcopy
from src.MC import attack

class QueueAttack:
    """ Queue for attacks """
    def __init__(self):
        """ Queue for attacks """
        self._attacks = {}
        self._to_remove = []

    def add_attack(self, attack:attack.Attack):
        """ Add to queue """
        self._attacks[attack._name] = deepcopy(attack)

    def delete_attack_from_queue(self, attack_name:str):
        """ Remove from queue """
        self._to_remove += attack_name

    def clear_attacks(self):
        """ Remove those attacks which finished recently """
        # Revisamos los ataques y si tienen duracion o ha caducado
        for name, attack in self._attacks.items():
            if attack._duration and attack._duration > 0:
                attack._duration -= 1
            else:
                self._to_remove += name
        while len(self._to_remove) > 0:
            name = self._to_remove.pop()
            del self._attacks[name]

    def in_queue(self, name):
        """ Checks if some attack it's in queue """
        return name in self._attacks
