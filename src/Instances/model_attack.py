""" Models based on attacks """
from src.MC import attack
from src.Instances.model_debuffs import *

light_attack = attack.Attack(
    name='Light attack', value=12500, duration=1, type='Direct damage'
)
wall_of_elements = attack.Attack(
    name='Wall of elements', value=2500, type='Direct damage', duration=10
)
mystic_orb = attack.Attack(
    name='Mystic orb', value=1200, type='Direct damage', duration=10
)
degeneration = attack.Attack(
    name='Degeneration', value=3480, type='Direct damage', duration=10
)
barbed_trap = attack.Attack(
    name='Barbed trap', value=2778, type='Direct damage', duration=16, debuf=minor_breach
)
blazing_spear = attack.Attack(
    name='Blazing Spear', value=300, type='Direct damage', duration=10
)
puncturing_sweep = attack.Attack(
    name='Puncturing Sweep', value=4000, type='Direct damage', duration=1
)
purifying_light = attack.Attack(
    name='Purifying Light', value=4774, type='Direct damage', duration=6
)
