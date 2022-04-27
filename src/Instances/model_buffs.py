""" Model for buffs and debuffs """
from src.MC import effects

minor_berserk = effects.Effect(
    name = 'Minor berserk',
    value = 5,
    mode = 'percent',
    stat_affected = 'damage',
    duration = 10,
    type = 'buff',
)