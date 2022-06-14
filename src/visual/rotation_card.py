import os
import json
import streamlit as st

def generate_rotation_card():
    """Rotation card""" 
    st.title(st.session_state['language_tags']["rotation_title"], anchor='center')
    selected = []
    cols = st.columns(6)
    main_abilities = []
    second_abilities = []
    list_of_skills = []

    if not st.session_state['character'].get('skills_order'):
        st.session_state['character']['skills_order'] = {
            'main': [st.session_state['skills_selected']['skills'][0]]*5,
            'second': [st.session_state['skills_selected']['skills'][0]]*5,
            'main_ultimate': st.session_state['skills_selected']['ultimate'][0],
            'second_ultimate': st.session_state['skills_selected']['ultimate'][0]
        }
        print(st.session_state['character']['skills_order'])

    if st.session_state.get('skills_selected'):
        with cols[0]:
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['main'][0]) or 0
            main_abilities.append(st.selectbox('main bar #1', st.session_state['skills_selected']['skills'], index=index))
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['second'][0]) or 0
            second_abilities.append(st.selectbox('second bar #1', st.session_state['skills_selected']['skills'], index=index))
        with cols[1]:
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['main'][1]) or 0
            main_abilities.append(st.selectbox('main bar #2', st.session_state['skills_selected']['skills'], index=index))
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['second'][1]) or 0
            second_abilities.append(st.selectbox('second bar #2', st.session_state['skills_selected']['skills'], index=index))
        with cols[2]:
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['main'][2]) or 0
            main_abilities.append(st.selectbox('main bar #3', st.session_state['skills_selected']['skills'], index=index))
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['second'][2]) or 0
            second_abilities.append(st.selectbox('second bar #3', st.session_state['skills_selected']['skills'], index=index))
        with cols[3]:
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['main'][3]) or 0
            main_abilities.append(st.selectbox('main bar #4', st.session_state['skills_selected']['skills'], index=index))
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['second'][3]) or 0
            second_abilities.append(st.selectbox('second bar #4', st.session_state['skills_selected']['skills'], index=index))
        with cols[4]:
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['main'][4]) or 0
            main_abilities.append(st.selectbox('main bar #5', st.session_state['skills_selected']['skills'], index=index))
            index = st.session_state['skills_selected']['skills'].index(st.session_state['character']['skills_order']['second'][4]) or 0
            second_abilities.append(st.selectbox('second bar #5', st.session_state['skills_selected']['skills'], index=index))
        with cols[5]:
            index = st.session_state['skills_selected']['ultimate'].index(st.session_state['character']['skills_order']['main_ultimate']) or 0
            main_ultimate = st.selectbox('main ultimate', st.session_state['skills_selected']['ultimate'], index=index)
            index = st.session_state['skills_selected']['ultimate'].index(st.session_state['character']['skills_order']['second_ultimate']) or 0
            second_ultimate = st.selectbox('second ultimate', st.session_state['skills_selected']['ultimate'], index=index)

        if None not in main_abilities:
            list_of_skills += list(main_abilities)
        if None not in second_abilities:
            list_of_skills += list(second_abilities)
        if main_ultimate is not None:
            list_of_skills += [main_ultimate]
        if second_ultimate is not None:
            list_of_skills += [second_ultimate]

        if not st.session_state['character'].get('rotation'):
            st.session_state['character']['rotation'] = []
        order = st.multiselect("Orden de habilidades", list_of_skills, default=st.session_state['character']['rotation'])

        st.session_state['rotation_selected'] = order
        st.write(' → '.join(order))

        st.session_state['character']['skills_available'] = st.session_state['skills_selected'].get('skills') + st.session_state['skills_selected'].get('ultimate')
        st.session_state['character']['passives_available'] = st.session_state['skills_selected'].get('passives')

        st.session_state['character']['skills_order'] = {
            'main': main_abilities,
            'second': second_abilities,
            'main_ultimate': main_ultimate,
            'second_ultimate': second_ultimate
        }

        st.session_state['character']['rotation'] = order
