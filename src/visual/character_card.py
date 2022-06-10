# pylint: disable=line-too-long
# pylint: disable=import-error
""" Visual interface for character """
import json

import streamlit as st

from src.visual.skill_card import clean_skills
from src.config.class_names import class_names
from src.config.races_names import races_names
from src.config.weapon_names import weapon_names
from src.config.buff_names import buff_names
from src.config.debuff_names import debuff_names

from src.utils.visual_utils import gen_spacing

def generate_character_card():
    """ Main method """
    data = {}
    if st.session_state.get('character_loaded') is None:
        st.session_state['character_loaded'] = True
    if st.session_state.get('character'):
        data = st.session_state['character']

    language_tags = st.session_state['language_tags']['character']
    # * All visual inputs
    data['name'] = st.text_input(language_tags['name'], value = data.get('name') or "")
    gen_spacing(2)
    with st.expander(language_tags['miscelaneo']):
        cols = st.columns(2)
        with cols[0]:
            races = races_names.index(data['races']) if data.get('races') else 0
            data['races'] = st.selectbox(language_tags['race'], races_names, on_change=clean_skills, index=races)

            main_bar = weapon_names.index(data['main_bar']) if data.get('main_bar') else 0
            data['main_bar'] = st.selectbox(language_tags['main_bar'], weapon_names, on_change=clean_skills, index=main_bar)

        with cols[1]:
            class_names_index = class_names.index(data['class']) if data.get('class') else 0
            data['class_name'] = st.selectbox(language_tags['class_name'], class_names, on_change=clean_skills, index=class_names_index)

            second_bar = weapon_names.index(data['second_bar']) if data.get('second_bar') else 0
            data['second_bar'] = st.selectbox(language_tags['second_bar'], weapon_names, on_change=clean_skills, index=second_bar)

    gen_spacing(2)
    with st.expander(language_tags['resources']):
        cols = st.columns(2)
        with cols[0]:
            data['max_magicka'] = st.text_input(language_tags['max_magicka'], value = data.get('max_magicka') or 12000)
            data['health'] = st.text_input(language_tags['max_health'], value = data.get('health') or 16000)
            data['max_stamina'] = st.text_input(language_tags['max_stamina'], value = data.get('max_stamina') or 12000)
        with cols[1]:
            data['magicka_recovery'] = st.text_input(language_tags['magicka_recovery'], value = data.get('magicka_recovery') or 514)
            data['health_recovery'] = st.text_input(language_tags['health_recovery'], value = data.get('health_recovery') or 309)
            data['stamina_recovery'] = st.text_input(language_tags['stamina_recovery'], value = data.get('stamina_recovery') or 514)

    gen_spacing(2)
    with st.expander(language_tags['damage']):
        cols = st.columns(2)
        with cols[0]:
            data['spell_damage'] = st.text_input(language_tags['spell_damage'], value = data.get('spell_damage') or 1000)
            data['spell_critical'] = st.text_input(language_tags['spell_critical'], value = data.get('spell_critical') or 10)
            data['spell_penetration'] = st.text_input(language_tags['spell_penetration'], value = data.get('spell_penetration') or 0)
        with cols[1]:
            data['weapon_damage'] = st.text_input(language_tags['weapon_damage'], value = data.get('physical_damage') or 1000)
            data['weapon_critical'] = st.text_input(language_tags['weapon_critical'], value = data.get('physical_critical') or 10)
            data['weapon_penetration'] = st.text_input(language_tags['physical_penetration'], value = data.get('physical_penetration') or 0)

    gen_spacing(2)
    with st.expander(language_tags['resistance']):
        cols = st.columns(2)
        with cols[0]:
            data['spell_resistance'] = st.text_input(language_tags['spell_resistance'], value = data.get('spell_resistance') or 0)
            data['critical_resistance'] = st.text_input(language_tags['critical_resistance'], value = data.get('critical_resistance') or 1320)
        with cols[1]:
            data['physical_resistance'] = st.text_input(language_tags['physical_resistance'], value = data.get('physical_resistance') or 0)

    gen_spacing(2)
    with st.expander('BUFFS & DEBUFFS - NO TAG'):
        data['buffs'] = st.multiselect('Buffs', buff_names)
        data['debuffs'] = st.multiselect('Debuffs', debuff_names)
    # * Save character to a file
    st.session_state['character'] = data
