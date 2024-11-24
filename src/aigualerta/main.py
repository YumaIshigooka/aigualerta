import streamlit as st
from aigualerta.services import tab_handler

# Execute the main with 'streamlit run .\src\interface\main.py' on the terminal

st.set_page_config(
    page_title="Aigualerta",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

tabs = st.tabs(["Welcome", "Upload/Process Data"])

tab_handler.init_session()
tab_handler.tab_handler(tabs)
