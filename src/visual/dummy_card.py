import os
import json
from io import StringIO
import streamlit as st

from src.models.dummy import Dummy

def effect_column_selector(buff:bool=True):
    """ Selector """
    if buff:
        title = 'Buff'
        folder_path = 'src/effects/buff'
    else:
        title = 'Debuff'
        folder_path = 'src/effects/debuff'
    files = os.listdir(folder_path)
    effect_names = [ s.replace('.json', '').replace('_', ' ').capitalize() for s in files ]
    selected_effects = st.multiselect(title, effect_names)
    for selected in selected_effects:
        st.text(selected)
    return selected_effects

def generate_dummy_card():
    data = {}
    if st.session_state.get('dummy'):
        data = st.session_state['dummy'].as_dict()

    # * Base card
    data['name'] = st.text_input("Name", value = data.get('name') or "Iron Atronach")
    cols = st.columns(2)
    with cols[0]:
        data['health'] = st.number_input("Max health", value = data.get('health') or 21000000)
    with cols[1]:
        data['base_resistance'] = st.number_input("Base armor resistance", value = data.get('base_resistance') or 18200)

    cols = st.columns(2)
    with cols[0]:
        data['buffs'] = effect_column_selector(buff=True)
    with cols[1]:
        data['debuffs'] = effect_column_selector(buff=False)

    # * Save dummy in session state
    st.session_state['dummy'] = Dummy(data)
    loading_dummy = st.sidebar.file_uploader('Load dummy')

    st.sidebar.download_button('Save dummy',
        json.dumps(st.session_state['dummy'].as_dict()),
        (st.session_state['dummy'].as_dict()['name']+'.json')
    )
    if loading_dummy:
        stringio = StringIO(loading_dummy.getvalue().decode("utf-8"))
        st.session_state['dummy'] = Dummy(json.loads(stringio.read()))
