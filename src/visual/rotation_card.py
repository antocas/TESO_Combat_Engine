import os
import json
from io import StringIO
import streamlit as st

from collections import OrderedDict

def generate_rotation_card():
    st.title(st.session_state['language_tags']["rotation_title"], anchor='center')
    selected = []
    if st.session_state.get('skills_selected'):
        if st.session_state['skills_selected'].get('skills_available'):
            min_rotation_buttons = min(10, len(st.session_state['skills_selected']['skills_available']))
            skills_available = st.session_state['skills_selected']['skills_available']
            for i in range(min_rotation_buttons):
                selected.append(st.selectbox(f'Selector {i+1}', skills_available))
    # st.session_state.['rotation'] = list(OrderedDict.fromkeys(selected))
    
    # * Save dummy in session state
    # st.session_state['dummy'] = Dummy(data)
    # loading_dummy = st.sidebar.file_uploader('Load dummy')

    # st.sidebar.download_button('Save dummy',
    #     json.dumps(st.session_state['dummy'].as_dict()),
    #     (st.session_state['dummy'].as_dict()['name']+'.json')
    # )
    # if loading_dummy:
    #     stringio = StringIO(loading_dummy.getvalue().decode("utf-8"))
    #     st.session_state['dummy'] = Dummy(json.loads(stringio.read()))
