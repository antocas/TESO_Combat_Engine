import streamlit as st

from src.common.visual_utils import gen_spacing
from src.visual.skill_card import generate_skill_card
from src.visual.skill_card import generate_skills_icons
from src.visual.dummy_card import generate_dummy_card
from src.visual.character_card import generate_character_card

from src.models.combat_simulator import main_combat

def sidebar_block():
    config = {}
    # options['']
    return st.sidebar.selectbox("Options", ('Character', 'Skills', 'Dummy'))

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

    if 'Character' == sidebar_block_option:
        generate_character_card()

    if 'Skills' == sidebar_block_option:
        generate_skill_card()

    if 'Dummy' == sidebar_block_option:
        generate_dummy_card()

    if st.sidebar.button('Refesh data'):
        st.experimental_rerun()
