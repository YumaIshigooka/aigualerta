import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, src_dir)

import streamlit as st
from interface import utils

# def upload_and_display_data():
#     """Uploads data and displays the raw dataframe."""
#     if st.session_state.user_df is not None:
#         st.subheader("Uploaded Dataset")
#         st.write(st.session_state.user_df.head())
#         return True
#     return False

# def process_and_display_data():
#     """Processes the data and displays the processed dataframe."""
#     if "user_df_setup" not in st.session_state:
#         st.session_state.user_df_setup = utils.setup_data(st.session_state.user_df)
#     if st.session_state.user_df_setup is not None:
#         st.subheader("Processed Dataset")
#         st.write(st.session_state.user_df_setup.head())
#         return True
#     return False

# def prepare_and_display_input():
#     """Prepares the input data and displays it."""
#     if "user_df_input" not in st.session_state:
#         st.session_state.user_df_input = utils.setup_input(st.session_state.user_df_setup)
#     if st.session_state.user_df_input is not None:
#         st.subheader("Input that will be used")
#         st.write(st.session_state.user_df_input.head())
#         return True
#     return False

# def predict_and_display_results():
#     """Handles prediction and displays the results."""
#     if st.button("Predict"):
#         st.session_state.user_df_predicted = utils.predict(st.session_state.user_df_input)
#         if st.session_state.user_df_predicted is not None:
#             st.subheader("Prediction Results")
#             st.write(st.session_state.user_df_predicted.head())

# def load_page():
#     """Loads the page and orchestrates the data flow."""
#     if upload_and_display_data():
#         if process_and_display_data():
#             if prepare_and_display_input():
#                 predict_and_display_results()
#     else:
#         st.write("If you are willing to **load your dataset from the data folder**, please refer to the *data from folder* tab.")

def load_page():

    # Upload data if not already done
    if st.session_state.user_df is None:
        st.session_state.user_df = utils.upload_data()

    if st.session_state.user_df is not None:
        st.subheader("Uploaded Dataset")
        st.write(st.session_state.user_df.head())

        # Process setup_data if not already done
        if st.session_state.user_df_setup is None:
            st.session_state.user_df_setup = utils.setup_data(st.session_state.user_df)

        if st.session_state.user_df_setup is not None:
            st.subheader("Processed Dataset")
            st.write(st.session_state.user_df_setup.head())

            # Process setup_input if not already done
            if st.session_state.user_df_input is None:
                st.session_state.user_df_input = utils.setup_input(st.session_state.user_df_setup)

            if st.session_state.user_df_input is not None:
                st.subheader("Input that will be used")
                st.write(st.session_state.user_df_input.head())

                # Handle prediction
                if st.button("Predict"):
                    st.session_state.user_df_predicted = utils.predict(st.session_state.user_df_input)

                # Show predictions if available
                if st.session_state.user_df_predicted is not None:
                    st.subheader("Prediction Results")
                    st.write(st.session_state.user_df_predicted.head())
    else:
        st.write("If you are willing to **load your dataset from the data folder**, please refer to the *data from folder* tab.")