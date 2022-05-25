""" Class attack """
from src.models.skill import Skill
class Attack:
    """ Class Attack """
    def __init__(self, kwargs):
        self.__attributes__ = kwargs
        # self._name = kwargs.get('name')
        # self._value = kwargs.get('value')
        # self._type = kwargs.get('type')
        # self._cast_time = kwargs.get('cast_time')
        # self._duration = kwargs.get('duration')
        # self._buffs = kwargs.get('bufs')
        # self._debuffs = kwargs.get('debufs')

    @classmethod
    def skill_to_attack(cls, skill: Skill):
        """ Return an array of Attacks based on some skill """
        # Array start at 1, range needs +1
        max_skill_coefs = int(skill.num_coef_vars) + 1
        range_of_coefs = range(1, max_skill_coefs)

        for index in range_of_coefs:
            data = {}
            data = skill.get_index_attributes( str(index) )
            data['name'] = f'{skill.name} {index}'
            data['duration'] = int(skill.duration)
            data['value'] = None
            attack = cls(data)

            yield attack

    def __str__(self) -> str:
        """ Return string """
        as_string = f"Name: {self.__attributes__['name']}, Duration: {self.__attributes__['duration']}"
        return as_string

    def as_dict(self):
        """ Return dict """
        return self.__attributes__

    @property
    def name(self):
        """ Name """
        return self.__attributes__["name"]

    @property
    def value(self):
        """ Value """
        return self.__attributes__["value"]

    @property
    def type_of_damage(self):
        """ Type of damage """
        return self.__attributes__["type_of_damage"]

    @property
    def cast_time(self):
        """ Cast Time """
        return self.__attributes__["cast_time"]

    @property
    def duration(self):
        """ Duration """
        return int(self.__attributes__["duration"])

    @property
    def buffs(self):
        """ Buffs """
        return self.__attributes__["buffs"]

    @property
    def debuffs(self):
        """ Debuffs """
        return self.__attributes__["debuffs"]

    def calculate_damage(self, max_resource, resource_damage, cap: int=1000000, index: int=1):
        skill_coef_max_resource = float(self.__attributes__[f'a{index}'])
        skill_coef_resource_damage = float(self.__attributes__[f'b{index}'])
        value = (skill_coef_max_resource * max_resource + skill_coef_resource_damage * resource_damage)
        self.__attributes__['value'] = min(int(value), cap)

    def decrease_attack_duration(self, seconds: int):
        """ Remove from queue """
        self.__attributes__['last_attack'] = seconds

        key = [key for key in self.__attributes__.keys() if key.startswith('duration_')]
        if key and self.__attributes__.get(key[0]) is not None:
            # Si tiene duracion propia del coef
            key = key[0]
            duration = int(self.__attributes__[key]) - 1000
            self.__attributes__[key] = duration
            self.__attributes__['duration'] = duration
        else:
            self.__attributes__['duration'] = self.__attributes__['duration'] - 1000

    def decrease_attack_delay(self, ):
        """ If an attack is delayed, decrease the delay """
        after = [after for after in self.__attributes__.keys() if after.startswith('after')][0]
        self.__attributes__[after] = int(self.__attributes__[after]) - 1000

    def make_critical(self, critical_damage: float):
        """ Make a critical attack """
        self.__attributes__['value'] = int(self.__attributes__['value'] * (1+critical_damage))

    def can_be_used(self, seconds: int):
        """ Can be used? """
        last_attack = self.__attributes__.get('last_attack')
        key = [key for key in self.__attributes__.keys() if key.startswith('tick_')]
        if key and self.__attributes__.get(key[0]) is not None:
            key = key[0]
        else:
            return True
        if last_attack is None:
            return True
        else:
            return (seconds - last_attack) >= self.__attributes__[key]

    def causes_damage(self):
        """ Returns true if has some sort of damage type """
        key = [key for key in self.__attributes__.keys() if key.startswith('type_of_damage_')]
        return bool( len(key) )
