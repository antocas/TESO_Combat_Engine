""" Model for buffs and debuffs """
from src.models import effects

minor_breach = effects.Effect(
    name = 'Minor breach',
    value = 2974,
    mode = 'fixed',
    stat_affected = 'spell_resistance',
    duration = 10,
    type = 'debuf',
)