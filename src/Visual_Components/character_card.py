import json
from io import StringIO

import streamlit as st

from src.Visual_Components.skill_card import clean_skills
from src.config.class_names import class_names
from src.config.weapon_names import weapon_names
from src.MC.character import Character

def block_load_data():
    st.session_state['character_loaded'] = not st.session_state['character_loaded']

def generate_character_card():
    data = {}
    if st.session_state.get('character_loaded') is None:
        st.session_state['character_loaded'] = True
    if st.session_state.get('character'):
        data = st.session_state['character'].attributes
    
    cols = st.columns(2)
    with cols[0]:
        data['name'] = st.text_input("Name", value = data.get('name') or "")
        try:
            data['class'] = st.selectbox("Class", class_names, on_change=clean_skills, index=class_names.index(data.get('class')))
        except:
            data['class'] = st.selectbox("Class", class_names)

    with cols[1]:
        try:
            data['main_bar'] = st.selectbox("Main bar", weapon_names, index=weapon_names.index(data.get('main_bar')))
        except Exception as e:
            data['main_bar'] = st.selectbox("Main bar", weapon_names)
        try:
            data['second_bar'] = st.selectbox("Second bar", weapon_names, index=weapon_names.index(data.get('second_bar')))
        except Exception as e:
            data['second_bar'] = st.selectbox("Second bar", weapon_names)

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
    loading_character = st.sidebar.file_uploader('Load character', disabled=not st.session_state['character_loaded'])
    st.sidebar.download_button('Save character',
        json.dumps(st.session_state['character'].as_dict()),
        (st.session_state['character'].name+'.json')
    )
    if loading_character and st.session_state['character_loaded']:
        stringio = StringIO(loading_character.getvalue().decode("utf-8"))
        st.session_state['character'] = Character(json.loads(stringio.read()))
        block_load_data()
