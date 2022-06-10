# pylint: disable=line-too-long
# pylint: disable=invalid-name
# pylint: disable=import-error
""" Skill Card """

import json
import os
import re

import pandas as pd
import streamlit as st
from src.config.visual_config import keys_to_import
from src.models.skill import Skill

@st.cache(suppress_st_warning=True)
def load_skill_by_type(skill_type: str = 'skill'):
    """ Load all skills sorted by type """
    skills = None
    base_path = "src/skills"
    files = os.listdir(f"{base_path}/{skill_type}")
    for file_name in files:
        with open(f"{base_path}/{skill_type}/{file_name}", 'r', encoding='utf-8') as file:
            skill_to_pandas = {}
            skill = json.load(file)
            for key, value in skill.items():
                if key in keys_to_import:
                    skill_to_pandas[key] = [value]

            if skills is None:
                skills = pd.DataFrame.from_dict(skill_to_pandas)
            else:
                prev_skill = pd.DataFrame.from_dict(skill_to_pandas)
                skills = pd.concat([skills, prev_skill], axis=0, ignore_index = True)
    return skills

def clean_skills():
    """ Clean skills """
    try:
        del st.session_state['skills_available']
    except KeyError:
        pass

def generate_skills_icons(skills_type='skills_available'):
    """ Load icons """
    if st.session_state.get('skills_selected'):
        images_cols = st.columns(10)
        i = 0
        for skill_name in st.session_state['skills_selected'][skills_type]:
            with images_cols[i]:
                img = st.session_state['skills_available'][skill_name].image
                st.image(img)
            i = i + 1

def generate_skill_in_columns(df_skills, key:str, default_values=[]):
    """ Generate all necessary selectors for the type of skills dessired """
    df = df_skills
    df = df.sort_values(['id'])
    branchs = df['skillLine'].unique()

    needed_cols = branchs.shape[0]
    if needed_cols == 0:
        return None
    cols = st.columns(needed_cols)
    skills_by_col = {}
    all_skills = []
    for index, col in enumerate(cols):
        with col:
            branch_name = branchs[index]
            branch = df[df['skillLine'] == branch_name]
            skill_names = []
            for _, row in branch.iterrows():
                skill_names.append(row['name'])
            skill_names =list(set(skill_names))
            skills_by_col[branch_name] = skill_names

            default_to_show = list(set(skills_by_col[branch_name]).intersection(set(default_values)))

            selected = st.multiselect(branch_name, skill_names, key=key, default=default_to_show)
            skills_by_col[branch_name] = selected
            all_skills += selected
    return all_skills

def filter_skill(to_filter, skill_type='', skill_line='', class_type='', race_type=''):
    """ Filter skills """
    filtered = to_filter
    if skill_type != '':
        filtered = filtered[filtered['skillType'] == skill_type]
    if skill_line != '':
        filtered = filtered[filtered['skillLine'] == skill_line]
    if class_type != '':
        filtered = filtered[filtered['classType'] == class_type]
    if race_type != '':
        filtered = filtered[filtered['raceType'] == race_type]
    return filtered

def generate_skill_card():
    """ Skill card """
    if st.session_state.get('skills_available') is None:
        st.session_state['skills_available'] = load_skill_by_type('skill')
    if st.session_state.get('passives_available') is None:
        st.session_state['passives_available'] = load_skill_by_type('passive')
    if st.session_state.get('ultimates_available') is None:
        st.session_state['ultimates_available'] = load_skill_by_type('ultimate')

    # * Check character exists
    if not st.session_state.get('character'):
        st.error('First, you need to create a character')
        return None
    if not st.session_state.get('skills_selected'):
        st.session_state['skills_selected'] = {}

    skill_class = filter_skill(st.session_state['skills_available'], skill_type='Class', class_type=st.session_state['character']['class_name'])
    skill_main_weapon = filter_skill(st.session_state['skills_available'], skill_line=st.session_state['character']["main_bar"])
    skill_second_weapon = filter_skill(st.session_state['skills_available'], skill_line=st.session_state['character']["second_bar"])
    skill_guild = filter_skill(st.session_state['skills_available'], skill_type='Guild')

    passive_class = filter_skill(st.session_state['passives_available'], skill_type='Class', class_type=st.session_state['character']['class_name'])
    passive_main_weapon = filter_skill(st.session_state['passives_available'], skill_line=st.session_state['character']["main_bar"])
    passive_second_weapon = filter_skill(st.session_state['passives_available'], skill_line=st.session_state['character']["second_bar"])
    passive_guild = filter_skill(st.session_state['passives_available'], skill_type='Guild')
    passive_race = filter_skill(st.session_state['passives_available'], skill_type='Racial', race_type=st.session_state['character']['races'])

    ultimate_class = filter_skill(st.session_state['ultimates_available'], skill_type='Class', class_type=st.session_state['character']['class_name'])
    ultimate_main_weapon = filter_skill(st.session_state['ultimates_available'], skill_line=st.session_state['character']["main_bar"])
    ultimate_second_weapon = filter_skill(st.session_state['ultimates_available'], skill_line=st.session_state['character']["second_bar"])
    ultimate_guild = filter_skill(st.session_state['ultimates_available'], skill_type='Guild')

    skills_selected = {}
    st.header('Skills')
    skills_selected['class skills'] = generate_skill_in_columns(skill_class, 'class skills', st.session_state['skills_selected'].get('class skills') or [])
    skills_selected['main bar skills'] = generate_skill_in_columns(skill_main_weapon, 'main bar skills', st.session_state['skills_selected'].get('main bar skills') or [])
    if st.session_state['character']['main_bar'] != st.session_state['character']['second_bar']:
        skills_selected['second bar skills'] = generate_skill_in_columns(skill_second_weapon, 'second bar skills', st.session_state['skills_selected'].get('second bar skills') or [])
    skills_selected['guild skills'] = generate_skill_in_columns(skill_guild, 'guild skills', st.session_state['skills_selected'].get('guild skills') or [])
    st.header('Passives')
    skills_selected['class passives'] = generate_skill_in_columns(passive_class, 'class passives', st.session_state['skills_selected'].get('class passives') or [])
    skills_selected['main bar passives'] = generate_skill_in_columns(passive_main_weapon, 'main bar passives', st.session_state['skills_selected'].get('main bar passives') or [])
    if st.session_state['character']['main_bar'] != st.session_state['character']['second_bar']:
        skills_selected['second bar passives'] = generate_skill_in_columns(passive_second_weapon, 'second bar passives', st.session_state['skills_selected'].get('second bar passives') or [])
    skills_selected['guild passives'] = generate_skill_in_columns(passive_guild, 'guild passives', st.session_state['skills_selected'].get('guild passives') or [])
    skills_selected['race passives'] = generate_skill_in_columns(passive_race, 'race passives', st.session_state['skills_selected'].get('race passives') or [])
    st.header('Ultimate')
    skills_selected['class ultimate'] = generate_skill_in_columns(ultimate_class, 'class skills ultimate', st.session_state['skills_selected'].get('class skills ultimate') or [])
    skills_selected['main bar ultimate'] = generate_skill_in_columns(ultimate_main_weapon, 'main bar ultimate', st.session_state['skills_selected'].get('main bar ultimate') or [])
    if st.session_state['character']['main_bar'] != st.session_state['character']['second_bar']:
        skills_selected['second bar ultimate'] = generate_skill_in_columns(ultimate_second_weapon, 'second bar ultimate', st.session_state['skills_selected'].get('second bar ultimate') or [])
    skills_selected['guild ultimate'] = generate_skill_in_columns(ultimate_guild, 'guild skills ultimate', st.session_state['skills_selected'].get('guild skills ultimate') or [])

    st.session_state['skills_selected'] = skills_selected

    return None
