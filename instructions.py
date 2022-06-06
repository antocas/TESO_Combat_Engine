""" Main app, streamlit runner """

import os
import json
import streamlit as st

from src.common.visual_utils import gen_spacing
from src.visual.skill_card import generate_skill_card
from src.visual.skill_card import generate_skills_icons
from src.visual.dummy_card import generate_dummy_card
from src.visual.rotation_card import generate_rotation_card
from src.visual.character_card import generate_character_card

from src.models.combat_simulator import main_combat

def sidebar_block():
    config = {}

    langs = [ s.replace('.json', '') for s in os.listdir('src/languages') ]

    config['language'] = st.sidebar.selectbox("Languages", langs)
    return config

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
    with open(f'src/languages/{language}.json', 'r', encoding='utf-8') as f:
        st.session_state['language_tags'] = json.load(f)

    if st.sidebar.button(st.session_state['language_tags']['refresh_data']):
        st.experimental_rerun()

    st.title(st.session_state['language_tags']["instructions"]['header'])
    st.subheader(st.session_state['language_tags']["instructions"]['subheader'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_1'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_2'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_3'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_4'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_5'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_6'])
    st.markdown(st.session_state['language_tags']["instructions"]['body_7'])
