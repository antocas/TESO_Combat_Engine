import streamlit as st

from src.MC.dummy import Dummy

def generate_dummy_card():
    data = {}
    if st.session_state.get('dummy'):
        data = st.session_state['dummy'].attributes
    
    data['name'] = st.text_input("Name", value = data.get('name') or "Iron Atronach")
    cols = st.columns(2)
    with cols[0]:
        data['health'] = st.text_input("Max health", value = data.get('health') or 21000000)
    with cols[1]:
        data['base_resistance'] = st.text_input("Base armor resistance", value = data.get('base_resistance') or 18200)

    if st.button("Save"):
        st.session_state['dummy'] = Dummy(data)