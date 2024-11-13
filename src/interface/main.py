import utils
import tabs
import streamlit as st

# Execute the main with 'streamlit run .\src\interface\main.py' on the terminal

st.set_page_config(
    page_title="Aigualerta",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TODO Define necessary tabs for the final project
tabs = utils.st.tabs(["Presentation", "Data Upload", "Dump data", "Loading data from path"])

for i, tab in enumerate(tabs):
    with tab:
        utils.load_page(i)
