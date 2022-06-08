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

    if st.session_state.get('skills_selected'):
        with cols[0]:
            main_abilities.add(st.selectbox('main bar #1', st.session_state['skills_selected']['skills']))
            second_abilities.add(st.selectbox('second bar #1', st.session_state['skills_selected']['skills']))
        with cols[1]:
            main_abilities.add(st.selectbox('main bar #2', st.session_state['skills_selected']['skills']))
            second_abilities.add(st.selectbox('second bar #2', st.session_state['skills_selected']['skills']))
        with cols[2]:
            main_abilities.add(st.selectbox('main bar #3', st.session_state['skills_selected']['skills']))
            second_abilities.add(st.selectbox('second bar #3', st.session_state['skills_selected']['skills']))
        with cols[3]:
            main_abilities.add(st.selectbox('main bar #4', st.session_state['skills_selected']['skills']))
            second_abilities.add(st.selectbox('second bar #4', st.session_state['skills_selected']['skills']))
        with cols[4]:
            main_abilities.add(st.selectbox('main bar #5', st.session_state['skills_selected']['skills']))
            second_abilities.add(st.selectbox('second bar #5', st.session_state['skills_selected']['skills']))
        with cols[5]:
            main_ultimate = st.selectbox('main ultimate', st.session_state['skills_selected']['ultimate'])
            second_ultimate = st.selectbox('second ultimate', st.session_state['skills_selected']['ultimate'])

        list_of_skills = list(main_abilities) + list(second_abilities) + [main_ultimate] + [second_ultimate]
        order = st.multiselect("Orden de habilidades", list_of_skills)
        if order is None:
            order = []
        st.session_state['rotation_selected'] = order
        st.write(', '.join(order))
