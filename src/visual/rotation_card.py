import os
import json
from io import StringIO
import streamlit as st

def generate_rotation_card():
    """Rotation card""" 
    st.title(st.session_state['language_tags']["rotation_title"], anchor='center')
    selected = []
    cols = st.columns(6)
    main_abilities = set()
    second_abilities = set()
    list_of_skills = []


    if st.session_state.get('skills_selected'):
        with cols[0]:
            main_abilities.add(st.selectbox('main bar #1', st.session_state['skills_selected'].get('skills')))
            second_abilities.add(st.selectbox('second bar #1', st.session_state['skills_selected'].get('skills')))
        with cols[1]:
            main_abilities.add(st.selectbox('main bar #2', st.session_state['skills_selected'].get('skills')))
            second_abilities.add(st.selectbox('second bar #2', st.session_state['skills_selected'].get('skills')))
        with cols[2]:
            main_abilities.add(st.selectbox('main bar #3', st.session_state['skills_selected'].get('skills')))
            second_abilities.add(st.selectbox('second bar #3', st.session_state['skills_selected'].get('skills')))
        with cols[3]:
            main_abilities.add(st.selectbox('main bar #4', st.session_state['skills_selected'].get('skills')))
            second_abilities.add(st.selectbox('second bar #4', st.session_state['skills_selected'].get('skills')))
        with cols[4]:
            main_abilities.add(st.selectbox('main bar #5', st.session_state['skills_selected'].get('skills')))
            second_abilities.add(st.selectbox('second bar #5', st.session_state['skills_selected'].get('skills')))
        with cols[5]:
            main_ultimate = st.selectbox('main ultimate', st.session_state['skills_selected'].get('ultimate'))
            second_ultimate = st.selectbox('second ultimate', st.session_state['skills_selected'].get('ultimate'))

        if None not in main_abilities:
            list_of_skills = list(main_abilities)
        if None not in second_abilities:
            list_of_skills += list(second_abilities)
        if main_ultimate is not None:
            list_of_skills = [main_ultimate]
        if second_ultimate is not None:
            list_of_skills += [second_ultimate]
        order = st.multiselect("Orden de habilidades", list_of_skills)
        st.session_state['rotation_selected'] = order
        st.write(', '.join(order))

        st.session_state['character']['skills_available'] = st.session_state['skills_selected'].get('skills') + st.session_state['skills_selected'].get('ultimate')
        st.session_state['character']['passives_available'] = st.session_state['skills_selected'].get('passives')
        st.session_state['character']['rotation'] = order
