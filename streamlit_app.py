import streamlit as st

from src.Visual_Components.character_card import generate_character_card


def sidebar_block():
    return st.sidebar.selectbox("Options", ('Dummy', 'Character', 'Skills'))

def dps_metric():
    columns = st.columns([2, 2, 6, 2])
    with columns[0]:
        st.metric(label="DPS", value="10k")
    with columns[1]:
        st.metric(label="Time", value="12 sec")
    with columns[3]:
        st.button('Calculate')

if __name__ == '__main__':
    st.set_page_config(layout="wide")
    dps_metric()
    if 'Character' == sidebar_block():
        generate_character_card()
