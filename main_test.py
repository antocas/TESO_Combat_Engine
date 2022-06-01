""" Main tester """

from json import load

from src.models.dummy import Dummy
from src.models.character import Character
from src.models.combat_simulator import main_combat

with open('files_for_testing/Olhena.json', encoding='utf-8') as f:
    character = Character(load(f)) # Load character from json

with open('files_for_testing/Iron Atronach.json', encoding='utf-8') as f:
    dummy = Dummy(load(f)) # Load dummy and passives from json

print(main_combat(character, dummy))
