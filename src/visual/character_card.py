import json
from io import StringIO

import streamlit as st

from src.visual.skill_card import clean_skills
from src.config.class_names import class_names
from src.config.races_names import races_names
from src.config.weapon_names import weapon_names
from src.models.character import Character

from src.common.visual_utils import gen_spacing

def block_load_data():
    st.session_state['character_loaded'] = not st.session_state['character_loaded']

def generate_character_card():
    data = {}
    if st.session_state.get('character_loaded') is None:
        st.session_state['character_loaded'] = True
    if st.session_state.get('character'):
        data = st.session_state['character'].attributes
    
    # * Load character from file
    loading_character = st.sidebar.file_uploader('Load character', on_change=block_load_data)
    if loading_character:
        stringio = StringIO(loading_character.getvalue().decode("utf-8"))
        data = json.loads(stringio.read())
        block_load_data()

    # * All visual inputs
    data['name'] = st.text_input("Name", value = data.get('name') or "")
    cols = st.columns(2)
    with cols[0]:
        try:
            data['races'] = st.selectbox("Races", races_names, on_change=clean_skills, index=races_names.index(data.get('races')))
        except:
            data['races'] = st.selectbox("Races", races_names, on_change=clean_skills)
        try:
            data['main_bar'] = st.selectbox("Main bar", weapon_names, on_change=clean_skills, index=weapon_names.index(data.get('main_bar')))
        except Exception as e:
            data['main_bar'] = st.selectbox("Main bar", weapon_names, on_change=clean_skills)

    with cols[1]:
        try:
            data['class'] = st.selectbox("Class", class_names, on_change=clean_skills, index=class_names.index(data.get('class')))
        except:
            data['class'] = st.selectbox("Class", class_names, on_change=clean_skills)
        try:
            data['second_bar'] = st.selectbox("Second bar", weapon_names, on_change=clean_skills, index=weapon_names.index(data.get('second_bar')))
        except Exception as e:
            data['second_bar'] = st.selectbox("Second bar", weapon_names, on_change=clean_skills)

    gen_spacing(3)
    cols = st.columns(2)
    with cols[0]:
        data['max_magicka'] = st.text_input("Max magicka", value = data.get('max_magicka') or 0)
        data['health'] = st.text_input("Max health", value = data.get('health') or 0)
        data['max_stamina'] = st.text_input("Max stamina", value = data.get('max_stamina') or 0)
        gen_spacing(3)
        data['spell_damage'] = st.text_input("Spell damage", value = data.get('spell_damage') or 0)
        data['spell_critical'] = st.text_input("Spell critical", value = data.get('spell_critical') or 0)
        data['spell_penetration'] = st.text_input("Spell penetration", value = data.get('spell_penetration') or 0)
        gen_spacing(3)
        data['spell_resistance'] = st.text_input("Spell resistance", value = data.get('spell_resistance') or 0)
        data['critical_resistance'] = st.text_input("Critical resistance", value = data.get('critical_resistance') or 0)
    with cols[1]:
        data['magicka_recovery'] = st.text_input("Magicka recovery", value = data.get('magicka_recovery') or 0)
        data['health_recovery'] = st.text_input("Health recovery", value = data.get('health_recovery') or 0)
        data['stamina_recovery'] = st.text_input("Stamina recovery", value = data.get('stamina_recovery') or 0)
        gen_spacing(3)
        data['physical_damage'] = st.text_input("Weapon damage", value = data.get('physical_damage') or 0)
        data['physical_critical'] = st.text_input("Weapon critical", value = data.get('physical_critical') or 0)
        data['physical_penetration'] = st.text_input("Physical penetration", value = data.get('physical_penetration') or 0)
        gen_spacing(3)
        data['physical_resistance'] = st.text_input("Physical resistance", value = data.get('physical_resistance') or 0)

    # * Save character to a file
    st.session_state['character'] = Character(data)
    st.sidebar.download_button('Save character',
        json.dumps(st.session_state['character'].as_dict()),
        (st.session_state['character'].name+'.json')
    )
