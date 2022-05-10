import os
import re
import json

# from src.config.class_names import class_names
from src.config.skills_names import skills_names
from src.mc.skill import Skill
import streamlit as st

def load_data_from_storage(skill_name):
    file_name = f'src/generators/skills/{skill_name}.json'.replace(' ', '_')
    skill = {}
    with open(file_name, 'r+', encoding='utf-8') as f:
        skill = json.load(f)
    return skill

def clean_skills():
    try:
        del st.session_state['skills_available']
    except:
        st.error('No skills loaded')

def generate_skills_icons():
    if st.session_state.get('skills_selected'):
        images_cols = st.columns(10)
        i = 0
        for skill in st.session_state['skills_selected']:
            with images_cols[i]:
                img = skill.image
                st.image(img)
            i = i + 1

def generate_skill_in_columns():
    pass

def generate_skill_card():
    # * Check character exists
    if not st.session_state.get('character'):
        st.error('First, you need to create a character')
        return None

    # * Check if skills are loaded, and load them
    if not st.session_state.get('skills_available'):
        st.session_state['skills_available'] = {}
        st.session_state['passives_available'] = {}

        skills_name = [ s.replace('.json', '').replace('_', ' ') for s in os.listdir('src/generators/skills') ]
        print(skills_name)

        for skill_name in skills_names:
            skill = load_data_from_storage(skill_name)
            if skill['classType'] == st.session_state['character'].class_name or skill['skillLine'] == st.session_state['character'].main_bar or skill['skillLine'] == st.session_state['character'].second_bar:
                if skill['isPassive'] == "0":
                    st.session_state['skills_available'][skill_name] = Skill(skill)
                else:
                    st.session_state['passives_available'][skill_name] = Skill(skill)
    # * Filter out necessary skills
    skills_names_plus = list(st.session_state['skills_available'].keys())
    selections = st.multiselect('Skill name', skills_names_plus)
    skills = {}
    st.session_state['skills_selected'] = [ st.session_state['skills_available'][skill_name] for skill_name in selections ]


    # * Show (as expandible) selected skills
    for skill_name in selections:
        with st.expander(skill_name):
            # print(st.session_state['skills_available'][skill_name])
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

    passives_names_plus = list(st.session_state['passives_available'].keys())
    selections = st.multiselect('Passives name', passives_names_plus)
    passives = {}
