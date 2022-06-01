""" Queue for attacks """
from copy import deepcopy
from src.models.attack import Attack

class QueueAttack:
    """ Queue for attacks """
    def __init__(self):
        """ Queue for attacks """
        self._attacks = {}
        self._to_remove = []

    def __str__(self):
        attacks = [name for name, attack in self._attacks.items()]
        return ', '.join(attacks)

    def add_attack(self, attack: Attack):
        """ Add to queue """
        self._attacks[attack.name] = deepcopy(attack)

    def remove_attack(self, name: str):
        """ Remove attack from queue """
        self._to_remove.append(name)

    def clear_attacks(self):
        """ Remove those attacks which finished recently """
        # Revisamos los ataques y si tienen duracion o ha caducado
        while len(self._to_remove) > 0:
            name = self._to_remove.pop()
            del self._attacks[name]

    def in_queue(self, name: str):
        """ Checks if some attack it's in queue """
        keys = self._attacks.keys()
        exits_some = False
        for key in keys:
            if key.lower().startswith(name):
                exits_some = True
                break

        return exits_some

    def next_attack(self):
        """ Returns the next attack """
        for key, value in self._attacks.items():
            yield (key, value)

    @property
    def attacks(self):
        """ Return attack in queue """
        return self._attacks
