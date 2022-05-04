import os
import re
import json

from src.config.class_names import class_names
from src.config.skills_names import skills_names
import streamlit as st

def load_data_from_storage(skill_name):
    file_name = f'src/Generators/Skills/{skill_name}.json'.replace(' ', '_')
    skill = {}
    with open(file_name, 'r+', encoding='utf-8') as f:
        skill = json.load(f)
    return skill

def clean_skills():
    try:
        del st.session_state['skills_available']
    except:
        st.alert('No skills loaded')

def generate_skill_card():
    selections = st.multiselect('Skill name', skills_names)
    skills = {}
    for selection in selections:
        if not skills.get(selection):
            skills[selection] = load_data_from_storage(selection)
    for skill_name, skill in skills.items():
        with st.expander(skill_name):
            skill['coefDescription'] = re.sub(r'\$\d', '{}', skill['coefDescription'])
            max_coefs = int(skill['numCoefVars']) + 1
            static_damages = []
            for coef in range(1, max_coefs):
                static_damage = f'staticDamage{coef}'
                skill[static_damage] = int(st.number_input(f'Valor {coef}', min_value=0, value=0, key=skill_name+static_damage))
                static_damages.append(str(skill[static_damage]))
            st.write( skill['coefDescription'].format(*static_damages) )

def generate_skill_card_plus():
    st.title('Esto es plus')
    if not st.session_state.get('character_class'):
        st.session_state['character_class'] = class_names[0]
    st.session_state['character_class'] = st.selectbox('Clase', class_names, on_change=clean_skills)
    if not st.session_state.get('skills_available'):
        st.session_state['skills_available'] = {}
        for skill_name in skills_names:
            skill = load_data_from_storage(skill_name)
            if skill['classType'] == st.session_state['character_class']:
                st.session_state['skills_available'][skill_name] = skill

    skills_names_plus = list(st.session_state['skills_available'].keys())
    selections = st.multiselect('Skill name', skills_names_plus)
    skills = {}
    for skill_name in selections:
        with st.expander(skill_name):
            st.session_state['skills_available'][skill_name]['coefDescription'] = re.sub(r'\$\d', '{}', st.session_state['skills_available'][skill_name]['coefDescription'])
            max_coefs = int(st.session_state['skills_available'][skill_name]['numCoefVars']) + 1
            static_damages = []
            for coef in range(1, max_coefs):
                static_damage = f'staticDamage{coef}'
                st.session_state['skills_available'][skill_name][static_damage] = int(st.number_input(f'Valor {coef}', min_value=0, value=0, key=skill_name+static_damage))
                static_damages.append(str(st.session_state['skills_available'][skill_name][static_damage]))
            st.write( st.session_state['skills_available'][skill_name]['coefDescription'].format(*static_damages) )