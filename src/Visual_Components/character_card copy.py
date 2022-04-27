import streamlit as st

from src.MC.character import Character

def generate_character_card():
    data = {}
    data['name'] = st.text_input("Name", value = "")
    cols = st.columns(3)
    with cols[0]:
        data['health'] = st.text_input("Max health", value = 0)
        data['spell_damage'] = st.text_input("Spell damage", value = 0)
        data['physical_damage'] = st.text_input("Weapon damage", value = 0)
    with cols[1]:
        data['max_magicka'] = st.text_input("Max magicka", value = 0)
        data['spell_critical'] = st.text_input("Spell critical", value = 0)
        data['physical_critical'] = st.text_input("Weapon critical", value = 0)
    with cols[2]:
        data['max_stamina'] = st.text_input("Max stamina", value = 0)
        data['spell_penetration'] = st.text_input("Spell penetration", value = 0)
        data['physical_penetration'] = st.text_input("Physical penetration", value = 0)

    if st.button("Save"):
        st.session_state['character'] = Character(data)
        print(st.session_state['character'])