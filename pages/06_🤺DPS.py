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

result = main_combat(character, dummy)
cols = st.columns(3)
with cols[0]:
    st.metric('DPS', result['dps'])
with cols[1]:
    st.metric('Minutes', result['minutes'])
with cols[2]:
    st.metric('Seconds', result['seconds'])
