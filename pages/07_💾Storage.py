"""Page for load/save in storage"""

import json
import time

from io import StringIO

import streamlit as st

data_to_safe = {
    "character": st.session_state.get('character'),
    "dummy": st.session_state.get('dummy'),
    "timestamp": time.asctime()
}

cols = st.columns(2)
with cols[0]:
    file = st.file_uploader("Upload configuration", ["json"], False)
    if file:
        stringio = StringIO(file.getvalue().decode("utf-8")).read()
        data_to_upload = json.loads(stringio)
        st.session_state['character'] = data_to_upload['character']
        st.session_state['dummy'] = data_to_upload['dummy']
    if st.session_state.get('character'):
        st.download_button("Save configuration", json.dumps(data_to_safe), f"{st.session_state['character']['name']}.json")
with cols[1]:
    st.text('Character')
    st.json(st.session_state.get('character'), expanded=False)
    st.text('Dummy')
    st.json(st.session_state.get('dummy'), expanded=False)
