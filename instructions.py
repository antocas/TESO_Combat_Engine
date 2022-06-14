""" Main app, streamlit runner """

import os
import json
import streamlit as st

from src.utils.visual_utils import gen_spacing
from src.utils.visual_utils import sidebar_block

from src.visual.skill_card import generate_skill_card
from src.visual.skill_card import generate_skills_icons
from src.visual.dummy_card import generate_dummy_card
from src.visual.rotation_card import generate_rotation_card
from src.visual.character_card import generate_character_card

from src.models.combat_simulator import main_combat



def dps_metric():
    columns = st.columns([2, 1, 2, 2, 2])
    with columns[0]:
        if st.button('Calculate'):
            with st.spinner('Calculating dps'):
                if st.session_state.get('dummy') and st.session_state.get('character'):
                    main_combat(st.session_state.get('dummy'), st.session_state.get('character'))
                else:
                    st.error('You need some data on your dummy or your character')
            st.experimental_rerun()
    with columns[2]:
        new = st.session_state.get('dps') or 0
        old = st.session_state.get('old_dps') or 0
        st.metric(label="DPS", value=new, delta=new-old)
        st.session_state['old_dps'] = new
    with columns[3]:
        new = st.session_state.get('time_minutes') or 0
        old = st.session_state.get('old_time_minutes') or 0
        st.metric(label="Time (minutes)", value=new, delta=new-old)
        st.session_state['old_time_minutes'] = new
    with columns[4]:
        new = st.session_state.get('time_seconds') or 0
        old = st.session_state.get('old_time_seconds') or 0
        st.metric(label="Time (seconds)", value=new, delta=new-old)
        st.session_state['old_time_seconds'] = new

if __name__ == '__main__':
    st.set_page_config(page_title="Combatest", page_icon='⚔️', layout="wide")
    # dps_metric()

    sidebar_block_option = sidebar_block()
    language = sidebar_block_option['language']

    st.title(st.session_state['language_tags']["instructions"]['header'])
    st.subheader(st.session_state['language_tags']["instructions"]['subheader'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_1'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_2'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_3'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_4'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_5'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_6'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_7'])

    if st.button(st.session_state['language_tags']['hero_of_tamriel']):
        with open('files_for_testing/hero_of_tamriel.json', 'r', encoding='utf-8') as file:
            json_file = json.load(file)
            st.session_state['character'] = json_file['character']
            st.session_state['dummy'] = json_file['dummy']
