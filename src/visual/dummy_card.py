import os
import json
from io import StringIO
import streamlit as st

from src.config.buff_names import buff_names
from src.config.debuff_names import debuff_names

from src.models.dummy import Dummy

def generate_dummy_card():
    """ Dummy card """
    data = {}
    if st.session_state.get('dummy'):
        data = st.session_state['dummy']

    # * Base card
    data['name'] = st.text_input("Name", value = data.get('name') or "Iron Atronach")
    cols = st.columns(2)
    with cols[0]:
        data['health'] = st.number_input("Max health", value = data.get('health') or 21000000)
    with cols[1]:
        data['base_resistance'] = st.number_input("Base armor resistance", value = data.get('base_resistance') or 18200)

    cols = st.columns(2)
    with cols[0]:
        data['buffs'] = st.multiselect('Buff', buff_names)
    with cols[1]:
        data['debuffs'] = st.multiselect('Debuff', debuff_names)

    # * Save dummy in session state
    st.session_state['dummy'] = data
