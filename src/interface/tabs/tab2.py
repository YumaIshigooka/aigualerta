import streamlit as st
import utils

def load_page():

    # Load data if not already loaded
    if st.session_state.df is None:
        st.session_state.df = utils.load_data_path()
        if st.session_state.df is None:
            st.error("Failed to load dataset. Please check that data source is stored in 'aigualerta/data/lectures_horaries_ABD.parquet' or upload your file on the **Data Upload** tab.")
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
        st.session_state.df_input = utils.setup_input(st.session_state.df_setup)
        st.subheader("Input that will be used")
        st.write(st.session_state.df_input.head())
        # Handle prediction
        if st.button("Predict"):
            st.session_state.df_predicted = utils.predict(st.session_state.df_input)
            st.subheader("Prediction Results")
            st.write(st.session_state.df_predicted.head())