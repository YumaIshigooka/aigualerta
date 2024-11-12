import streamlit as st
import utils

def load_page():

    df = utils.upload_data()

    if df is not None:
        df = utils.adapt_data(df)