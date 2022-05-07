""" Class attack """

class Attack:
    def __init__(self, **kwargs):
        self._name = kwargs.get('name')
        self._value = kwargs.get('value')
        self._type = kwargs.get('type')
        self._cast_time = kwargs.get('cast_time')
        self._duration = kwargs.get('duration')
        self._buffs = kwargs.get('bufs')
        self._debuffs = kwargs.get('debufs')

