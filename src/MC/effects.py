""" Effect class """

class Effect:
    """ Effect class """
    def __init__(self, **kwargs):
        """ Effect class """
        self._name = kwargs.get('name')
        self._value = kwargs.get('value')
        self._stat_affected = kwargs.get('stat_affected')
        self._mode = kwargs.get('mode') # Porcentaje o fijo
        self._duration = kwargs.get('duration') # Tiempo del efecto
        self._type = kwargs.get('type') # Buff o debuff -> pinta inutil

    def __str__(self) -> str:
        """ Str effect """
        string = f'Name: {self._name}\nValue: {self._value}\nStat affected {self.stat_affected}\nMode: {self._mode}\nDuration: {self._duration}\nType: {self._type}\n'
        return string

    def decrease_duration(self):
        self._duration -= 1

    # function to get value of _name
    def get_name(self):
        return self._name
    
    # function to get value of _value
    def get_value(self):
        return self._value
    
    # function to get value of _stat_affected
    def get_stat_affected(self):
        return self._stat_affected

    # function to get value of _mode
    def get_mode(self):
        return self._mode

    # function to get value of _duration
    def get_duration(self):
        return self._duration
    
    # function to get value of _type
    def get_type(self):
        return self._type

    name = property(get_name)
    value = property(get_value)
    stat_affected = property(get_stat_affected)
    mode = property(get_mode)
    duration = property(get_duration)
    type = property(get_type)
