""" Models based on attacks """
from src.MC import attack
from src.Instances.model_debuffs import *

light_attack = attack.Attack(
    name='Light attack', value=5000, duration=1, type='Direct damage'
)
wall_of_elements = attack.Attack(
    name='Wall of elements', value=2500, type='Direct damage', duration=10
)
mystic_orb = attack.Attack(
    name='Mystic orb', value=1200, type='Direct damage', duration=10
)
barbed_trap = attack.Attack(
    name='Barbed trap', value=0, type='Direct damage', duration=16, debuf=minor_breach
)