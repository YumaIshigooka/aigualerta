import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, src_dir)

import streamlit as st
from interface import utils

def load_page():

    # Load data if not already loaded
    if st.session_state.df is None:
        st.session_state.df = utils.load_data_path()
        if st.session_state.df is None:
            st.error("Failed to load dataset. Please check that data source is stored in 'aigualerta/data/lectures_horaries_ABD.parquet'.")
            return

    # Display raw data
    st.subheader("Raw Dataset")
    st.write(st.session_state.df.head())

    # Process setup_data if not already done
    if st.session_state.df_setup is None:
        st.session_state.df_setup = utils.setup_data(st.session_state.df)

    if st.session_state.df_setup is not None:
        st.subheader("Processed dataset")
        st.write(st.session_state.df_setup.head())

        # Process setup_input if not already done
        if st.session_state.df_input is None:
            st.session_state.df_input = utils.setup_input(st.session_state.df_setup)

        if st.session_state.df_input is not None:
            st.subheader("Input that will be used")
            st.write(st.session_state.df_input.head())

            # Handle prediction
            if st.button("Predict"):
                st.session_state.df_predicted = utils.predict(st.session_state.df_input)

            # Show predictions if available
            if st.session_state.df_predicted is not None:
                st.subheader("Prediction Results")
                st.write(st.session_state.df_predicted.head())