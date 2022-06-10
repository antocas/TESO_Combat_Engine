"""Page for load/save in storage"""

import json
import streamlit as st


cols = st.columns(2)
with cols[0]:
    st.file_uploader("Upload configuration", ["json"], False)
    st.download_button("Save configuration", json.dumps({}))
with cols[1]:
    st.text('Character')
    st.json(st.session_state.get('character'), expanded=False)
    st.text('Dummy')
    st.json(st.session_state.get('dummy'), expanded=False)
