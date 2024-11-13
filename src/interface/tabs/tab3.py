import streamlit as st
import utils

def load_page():

    df = utils.load_data_path()

    if df is not None:
        df = utils.setup_data(df)
        if df is not None:
            df = utils.setup_input(df)