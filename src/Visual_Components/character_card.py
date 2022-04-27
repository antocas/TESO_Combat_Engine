import json
from io import StringIO

import streamlit as st

from src.MC.character import Character

def generate_character_card():
    data = {}
    if st.session_state.get('character'):
        data = st.session_state['character'].attributes
    
    data['name'] = st.text_input("Name", value = data.get('name') or "")
    
    cols = st.columns(3)
    with cols[0]:
        data['health'] = st.text_input("Max health", value = data.get('health') or 0)
        data['spell_damage'] = st.text_input("Spell damage", value = data.get('spell_damage') or 0)
        data['physical_damage'] = st.text_input("Weapon damage", value = data.get('physical_damage') or 0)
    with cols[1]:
        data['max_magicka'] = st.text_input("Max magicka", value = data.get('max_magicka') or 0)
        data['spell_critical'] = st.text_input("Spell critical", value = data.get('spell_critical') or 0)
        data['physical_critical'] = st.text_input("Weapon critical", value = data.get('physical_critical') or 0)
    with cols[2]:
        data['max_stamina'] = st.text_input("Max stamina", value = data.get('max_stamina') or 0)
        data['spell_penetration'] = st.text_input("Spell penetration", value = data.get('spell_penetration') or 0)
        data['physical_penetration'] = st.text_input("Physical penetration", value = data.get('physical_penetration') or 0)

    st.session_state['character'] = Character(data)
    loading_character = st.sidebar.file_uploader('Load character')
    st.sidebar.download_button('Save character',
        json.dumps(st.session_state['character'].as_dict()),
        (st.session_state['character'].name+'.json')
    )
    if loading_character:
        stringio = StringIO(loading_character.getvalue().decode("utf-8"))
        st.session_state['character'] = Character(json.loads(stringio.read()))
