import os
import json
from io import StringIO
import streamlit as st

def generate_rotation_card():
    st.title(st.session_state['language_tags']["rotation_title"], anchor='center')
    selected = []
    cols = st.columns(6)
    main_abilities = set()
    second_abilities = set()
    list_of_skills = []


    if st.session_state.get('skills_selected'):
        skills_keys = [key for key in st.session_state['skills_selected'].keys() if key.endswith('skills')]
        skills_selected = [skill for skill_type in skills_keys for skill in st.session_state['skills_selected'][skill_type]]

        passives_keys = [key for key in st.session_state['skills_selected'].keys() if key.endswith('passives')]
        passives_selected = [skill for skill_type in passives_keys for skill in st.session_state['skills_selected'][skill_type]]

        ultimate_keys = [key for key in st.session_state['skills_selected'].keys() if key.endswith('ultimate')]
        ultimate_selected = [skill for skill_type in ultimate_keys for skill in st.session_state['skills_selected'][skill_type]]

        with cols[0]:
            main_abilities.add(st.selectbox('main bar #1', skills_selected))
            second_abilities.add(st.selectbox('second bar #1', skills_selected))
        with cols[1]:
            main_abilities.add(st.selectbox('main bar #2', skills_selected))
            second_abilities.add(st.selectbox('second bar #2', skills_selected))
        with cols[2]:
            main_abilities.add(st.selectbox('main bar #3', skills_selected))
            second_abilities.add(st.selectbox('second bar #3', skills_selected))
        with cols[3]:
            main_abilities.add(st.selectbox('main bar #4', skills_selected))
            second_abilities.add(st.selectbox('second bar #4', skills_selected))
        with cols[4]:
            main_abilities.add(st.selectbox('main bar #5', skills_selected))
            second_abilities.add(st.selectbox('second bar #5', skills_selected))
        with cols[5]:
            main_ultimate = st.selectbox('main ultimate', ultimate_selected)
            second_ultimate = st.selectbox('second ultimate', ultimate_selected)

        if None not in main_abilities:
            list_of_skills += list(main_abilities)
        if None not in second_abilities:
            list_of_skills += list(second_abilities)
        if main_ultimate is not None:
            list_of_skills += [main_ultimate]
        if second_ultimate is not None:
            list_of_skills += [second_ultimate]
        order = st.multiselect("Orden de habilidades", list_of_skills)
        st.session_state['rotation_selected'] = order
        st.write(', '.join(order))

        st.session_state['character']['skills_available'] = skills_selected + ultimate_selected
        st.session_state['character']['passives_available'] = passives_selected
        st.session_state['character']['rotation'] = order
