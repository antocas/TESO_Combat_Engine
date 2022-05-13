24129140

import os
import re
import json

from src.config.class_names import class_names
from src.models.skill import Skill
import streamlit as st

def load_data_from_storage(skill_name):
    file_name = f'src/skills/{skill_name}.json'.replace(' ', '_')
    skill = {}
    with open(file_name, 'r+', encoding='utf-8') as f:
        skill = json.load(f)
    return skill

def clean_skills():
    try:
        del st.session_state['skills_available']
    except:
        st.error('No skills loaded')

def generate_skills_icons(skills_type='skills_available'):
    if st.session_state.get('skills_selected'):
        images_cols = st.columns(10)
        i = 0
        print(st.session_state['skills_selected'][skills_type])
        for skill_name in st.session_state['skills_selected'][skills_type]:
            with images_cols[i]:
                img = st.session_state['skills_available'][skill_name].image
                st.image(img)
            i = i + 1

def generate_skill_in_columns(skills_type='skills_available'):
    ordered_skills = {}
    if st.session_state.get(skills_type):
        skills_selected = set()
        for k, v in st.session_state[skills_type].items():
            if not ordered_skills.get(v.skill_type):
                ordered_skills[v.skill_type] = {}
            if not ordered_skills[v.skill_type].get(v.skill_line):
                ordered_skills[v.skill_type][v.skill_line] = []
            ordered_skills[v.skill_type][v.skill_line].append(v)

        formated_skills_selectors = ['Class', 'Weapon', 'Guild', 'Craft']
        for selector in formated_skills_selectors:
            # * Exponemos las habilidades en n buscadores
            try:
                class_names = ordered_skills[selector].keys()
            except:
                break
            columns = st.columns(len(class_names))
            i = 0
            for name in sorted(class_names):
                with columns[i]:
                    skills_from_class = [ skill.name for skill in ordered_skills[selector][name] ]
                    p = st.multiselect(name, skills_from_class)
                    p = set(p)
                    skills_selected.update(p)
                i = i+1
        st.session_state['skills_selected'][skills_type] = list(skills_selected)

def filter_skills():
    skills_names = [ s.replace('.json', '').replace('_', ' ') for s in os.listdir('src/skills') ]
    for skill_name in skills_names:
        skill = load_data_from_storage(skill_name)
        # * Hablidades de arma
        if skill['skillLine'] == st.session_state['character'].main_bar or skill['skillLine'] == st.session_state['character'].second_bar:
            if skill['isPassive'] == "0":
                st.session_state['weapon_skills_available'][skill_name] = Skill(skill)
            else:
                st.session_state['weapon_passives_available'][skill_name] = Skill(skill)
        # * Crafteo y guilds
        if skill['skillType'] == "Craft" or skill['skillType'] == "Guild":
            if skill['isPassive'] == "0":
                st.session_state['miscelaneo_skills_available'][skill_name] = Skill(skill)
            else:
                st.session_state['miscelaneo_passives_available'][skill_name] = Skill(skill)
        # * De clase
        if skill['classType'] == st.session_state['character'].class_name:
            if skill['isPassive'] == "0":
                st.session_state['character_skills_available'][skill_name] = Skill(skill)
            else:
                st.session_state['character_passives_available'][skill_name] = Skill(skill)

def generate_skill_card():
    # * Check character exists
    if not st.session_state.get('character'):
        st.error('First, you need to create a character')
        return None

    # * Check if skills are loaded, and load them
    if not st.session_state.get('skills_available'):
        st.session_state['skills_available'] = {}
        st.session_state['passives_available'] = {}
        st.session_state['skills_selected'] = {}
        st.session_state['weapon_skills_available'] = {}
        st.session_state['weapon_passives_available'] = {}
        st.session_state['miscelaneo_skills_available'] = {}
        st.session_state['miscelaneo_passives_available'] = {}
        st.session_state['character_skills_available'] = {}
        st.session_state['character_passives_available'] = {}

        # * Filter out necessary skills
        filter_skills()
    
    # * TEMPORAL
    st.session_state['skills_available'] = {
        **st.session_state['weapon_skills_available'],
        **st.session_state['miscelaneo_skills_available'],
        **st.session_state['character_skills_available']
    }
    
    st.session_state['passives_available'] = {
        **st.session_state['weapon_passives_available'],
        **st.session_state['miscelaneo_passives_available'],
        **st.session_state['character_passives_available'],
    }

    st.header('Skills')
    generate_skill_in_columns(skills_type='skills_available')

    # * Show (as expandible) selected skills
    for skill_name in st.session_state['skills_selected']['skills_available']:
        cols = st.columns((1, 11))
        with cols[0]:
            # Icon
            img = st.session_state['skills_available'][skill_name].image
            st.image(img)
        with cols[1]:
            with st.expander(skill_name):
                # Substitude $1 and alike for {}
                coef_description = re.sub(r'\$\d', '{}', st.session_state['skills_available'][skill_name].coef_description)
                if coef_description == '':
                    st.caption(st.session_state['skills_available'][skill_name].description)
                else:
                    # Calculate damage
                    st.session_state['skills_available'][skill_name].calculate_coefs(st.session_state['character'])
                    # Damage
                    damage = st.session_state['skills_available'][skill_name].get_calculated_damage()
                    # Format output text
                    st.caption(coef_description.format(*damage))

    st.header('Passives')
    generate_skill_in_columns(skills_type='passives_available')