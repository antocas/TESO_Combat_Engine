import streamlit as st


from src.common.visual_utils import sidebar_block
from src.visual.character_card import generate_character_card

sidebar_block()
generate_character_card()
