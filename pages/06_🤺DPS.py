""" DPS page """
from copy import deepcopy
import streamlit as st

from src.models.dummy import Dummy
from src.models.character import Character
from src.models.combat_simulator import main_combat

plain_character = deepcopy(st.session_state['character'])
plain_dummy = deepcopy(st.session_state['dummy'])
character = Character(plain_character) # Load character from json
dummy = Dummy(plain_dummy) # Load dummy and passives from json

print(main_combat(character, dummy))
