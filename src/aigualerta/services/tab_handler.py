import streamlit as st
from aigualerta import utils
from aigualerta.tabs import tab0, tab1, tab2

tabs = [tab0, tab1, tab2]

def tab_handler(st_tabs):
    for i, tab in enumerate(st_tabs):
        with tab:
            tabs[i].load_page()

# def load_page(i):
#     tabs[i].load_page()

def init_session():
    if "show_dump_plot" not in st.session_state:
        st.session_state["show_dump_plot"] = False  # Default is hidden
    if "df" not in st.session_state:
        st.session_state.df = None
    if "setup_df" not in st.session_state:
        st.session_state.setup_df = None
    if "input_df" not in st.session_state:
        st.session_state.input_df = None
    if "predicted_df" not in st.session_state:
        st.session_state.predicted_df = None
    if "user_df" not in st.session_state:
        st.session_state.user_df = None
    if "user_df_setup" not in st.session_state:
        st.session_state.user_df_setup = None
    if "user_df_input" not in st.session_state:
        st.session_state.user_df_input = None
    if "user_df_predicted" not in st.session_state:
        st.session_state.user_df_predicted = None