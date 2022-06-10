import streamlit as st

from src.common.visual_utils import sidebar_block
from src.visual.skill_card import generate_skill_card

sidebar_block()
generate_skill_card()
