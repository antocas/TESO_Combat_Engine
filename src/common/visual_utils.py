""" Common effects and utils """ 
import streamlit as st

def gen_spacing(n_of_spaces=3):
    """ Generate spacing for Streamlit """
    for _ in range(n_of_spaces):
        st.text("")
class BColors:
    """ Class for use colors in terminal """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
