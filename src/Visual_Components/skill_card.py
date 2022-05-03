import os
import json

from src.config.skills_names import skills_names
import streamlit as st

def load_data_from_storage(skill_name):
    file_name = f'src/Generators/Skills/{skill_name}.json'.replace(' ', '_')
    skill = {}
    with open(file_name, 'r+', encoding='utf-8') as f:
        skill = json.load(f)
    return skill

def generate_skill_card():
    selections = st.multiselect('Skill name', skills_names)
    skills = {}
    for selection in selections:
        if not skills.get(selection):
            skills[selection] = load_data_from_storage(selection)
        st.text( skills[selection]['rawDescription'] )